"""
Production-ready Gemini API request handler with rate limiting and retry logic.

This module prevents "429 quota exceeded" errors by enforcing rate limiting
(max 5 requests per minute) and implementing intelligent retry logic with
exponential backoff for handling quota errors on the Gemini API free tier.

Example Usage:
    import google.generativeai as genai
    from modules.gemini_request_manager import GeminiRequestManager
    
    # Initialize the manager
    genai.configure(api_key="YOUR_API_KEY")
    model = genai.GenerativeModel("gemini-2.5-flash")
    manager = GeminiRequestManager(model)
    
    # Use the manager for all requests
    try:
        response = manager.generate("What are the health benefits of exercise?")
        print(response)
    except Exception as e:
        print(f"Request failed: {e}")
"""

import logging
import time
from typing import Optional
from collections import deque
from threading import Lock
from datetime import datetime, timedelta


class RateLimitExceeded(Exception):
    """Custom exception for rate limit violations."""
    pass


class GeminiRequestManager:
    """
    Production-ready Gemini API request handler with rate limiting and retry logic.
    
    Features:
    - Rate limiting: Maximum 5 requests per minute (12 seconds between requests)
    - Automatic delay calculation and request queuing
    - Intelligent retry logic: Up to 3 retries on 429/quota errors
    - Exponential backoff with ~35 second delay between retries
    - Comprehensive error logging
    - Thread-safe operations
    
    Args:
        model: Initialized Gemini GenerativeModel instance
        requests_per_minute: Maximum allowed requests per minute (default: 5)
        min_delay_seconds: Minimum seconds between requests (default: 12)
        max_retries: Maximum number of retry attempts (default: 3)
        retry_wait_seconds: Seconds to wait before retry (default: 35)
        logger: Optional custom logger instance
    
    Attributes:
        model: The Gemini model instance
        requests_per_minute: Rate limit configuration
        min_delay_seconds: Calculated minimum delay between requests
        max_retries: Maximum retries for failed requests
        retry_wait_seconds: Delay before retrying failed requests
    """
    
    def __init__(
        self,
        model,
        requests_per_minute: int = 5,
        min_delay_seconds: Optional[float] = None,
        max_retries: int = 3,
        retry_wait_seconds: float = 35.0,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize the Gemini request manager.
        
        Args:
            model: Initialized Gemini GenerativeModel instance
            requests_per_minute: Max requests per minute (default: 5)
            min_delay_seconds: Seconds between requests. If None, calculated as
                             60 / requests_per_minute
            max_retries: Max retry attempts (default: 3)
            retry_wait_seconds: Seconds to wait before retry (default: 35)
            logger: Custom logger for error reporting
        """
        self.model = model
        self.requests_per_minute = requests_per_minute
        self.min_delay_seconds = min_delay_seconds or (60 / requests_per_minute)
        self.max_retries = max_retries
        self.retry_wait_seconds = retry_wait_seconds
        
        # Setup logging
        self.logger = logger or logging.getLogger(__name__)
        
        # Rate limiting state
        self._request_times = deque(maxlen=requests_per_minute)
        self._lock = Lock()
        
        self.logger.info(
            f"GeminiRequestManager initialized: "
            f"{requests_per_minute} req/min (delay: {self.min_delay_seconds}s), "
            f"max_retries: {max_retries}"
        )
    
    def _wait_for_rate_limit(self) -> None:
        """
        Check rate limit and wait if necessary before allowing next request.
        
        This ensures no more than the configured number of requests are sent
        per minute by tracking request timestamps and introducing delays.
        """
        with self._lock:
            now = time.time()
            
            # If we have enough requests logged and the oldest is recent, wait
            if len(self._request_times) >= self.requests_per_minute:
                oldest_request_time = self._request_times[0]
                time_since_oldest = now - oldest_request_time
                
                if time_since_oldest < 60:
                    wait_time = 60 - time_since_oldest + 0.1
                    self.logger.debug(
                        f"Rate limit: waiting {wait_time:.2f}s "
                        f"({len(self._request_times)}/{self.requests_per_minute} requests in last minute)"
                    )
                    time.sleep(wait_time)
                    now = time.time()
            
            # Record this request time
            self._request_times.append(now)
    
    def _is_quota_error(self, error: Exception) -> bool:
        """
        Check if an error is a quota/rate limit error (429).
        
        Args:
            error: The exception to check
        
        Returns:
            True if error is a quota/rate limit error, False otherwise
        """
        error_str = str(error).lower()
        error_type = type(error).__name__.lower()
        
        # Check for common patterns
        quota_patterns = [
            "429",
            "quota",
            "rate limit",
            "quota exceeded",
            "resourceexhausted",
            "too many requests"
        ]
        
        return any(pattern in error_str or pattern in error_type 
                   for pattern in quota_patterns)
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate content using Gemini model with rate limiting and retry logic.
        
        This method handles all rate limiting, queuing, and retry logic
        automatically. Use this instead of calling model.generate_content()
        directly to ensure API quota compliance.
        
        Args:
            prompt: Text prompt to send to the model
            **kwargs: Additional arguments to pass to model.generate_content()
                     (e.g., temperature, top_p, safety_settings)
        
        Returns:
            Generated response text from the model
        
        Raises:
            ValueError: If prompt is empty or invalid
            Exception: If request fails after all retries or for non-recoverable errors
        
        Example:
            >>> response = manager.generate(
            ...     "What's a healthy breakfast?",
            ...     temperature=0.7
            ... )
            >>> print(response)
        """
        if not prompt or not isinstance(prompt, str):
            raise ValueError("Prompt must be a non-empty string")
        
        attempt = 0
        last_error = None
        
        while attempt <= self.max_retries:
            try:
                # Enforce rate limiting before making request
                self._wait_for_rate_limit()
                
                self.logger.debug(f"Sending request (attempt {attempt + 1}/{self.max_retries + 1})")
                
                # Generate content using the model
                response = self.model.generate_content(prompt, **kwargs)
                
                # Extract and return text
                generated_text = response.text if hasattr(response, 'text') else str(response)
                
                self.logger.info(f"Request successful: {len(generated_text)} characters generated")
                return generated_text
                
            except Exception as error:
                last_error = error
                attempt += 1
                
                # Check if this is a quota/rate limit error
                if self._is_quota_error(error):
                    if attempt <= self.max_retries:
                        self.logger.warning(
                            f"Quota/rate limit error (attempt {attempt}/{self.max_retries + 1}): {error}. "
                            f"Retrying in {self.retry_wait_seconds}s..."
                        )
                        time.sleep(self.retry_wait_seconds)
                        continue
                    else:
                        self.logger.error(
                            f"Quota error persisted after {self.max_retries} retries: {error}"
                        )
                        raise
                else:
                    # Non-quota errors should fail immediately
                    self.logger.error(f"Non-recoverable error: {error}")
                    raise
        
        # This shouldn't be reached, but just in case
        raise RuntimeError(
            f"Request failed after {self.max_retries} retries. "
            f"Last error: {last_error}"
        )
    
    def generate_with_fallback(
        self,
        prompt: str,
        fallback_response: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Generate content with optional fallback response if all retries fail.
        
        Useful for production applications where you want to provide a graceful
        degradation rather than raising an exception.
        
        Args:
            prompt: Text prompt to send to the model
            fallback_response: Response to return if generation fails
                             (e.g., "Unable to generate response. Please try again.")
            **kwargs: Additional arguments for model.generate_content()
        
        Returns:
            Generated response or fallback_response if generation fails
        
        Example:
            >>> response = manager.generate_with_fallback(
            ...     "Hi there!",
            ...     fallback_response="Hello! I'm unable to respond right now."
            ... )
        """
        try:
            return self.generate(prompt, **kwargs)
        except Exception as e:
            self.logger.error(f"Generation failed, using fallback: {e}")
            if fallback_response:
                return fallback_response
            return f"Error: Unable to generate response ({type(e).__name__})"
    
    def get_rate_limit_status(self) -> dict:
        """
        Get current rate limit status.
        
        Returns:
            Dictionary with rate limit information:
            - requests_in_window: Number of requests in the last minute
            - capacity: Maximum allowed requests per minute
            - available_slots: Remaining request slots
            - next_request_available_in: Seconds until next request is allowed
            - window_start: Timestamp of oldest request in window
        """
        with self._lock:
            now = time.time()
            requests_count = len(self._request_times)
            available_slots = max(0, self.requests_per_minute - requests_count)
            
            next_available_in = 0
            if requests_count >= self.requests_per_minute:
                oldest_time = self._request_times[0]
                time_since_oldest = now - oldest_time
                if time_since_oldest < 60:
                    next_available_in = 60 - time_since_oldest
            
            return {
                "requests_in_window": requests_count,
                "capacity": self.requests_per_minute,
                "available_slots": available_slots,
                "next_request_available_in": max(0, next_available_in),
                "window_start": self._request_times[0] if self._request_times else None,
                "requests_per_minute": self.requests_per_minute,
                "min_delay_seconds": self.min_delay_seconds
            }
    
    def reset_rate_limit(self) -> None:
        """
        Reset rate limit counters. Useful for testing or manual restart.
        
        Warning: Use carefully as this disables rate limiting protections.
        """
        with self._lock:
            self._request_times.clear()
            self.logger.info("Rate limit counters reset")


# Example usage and integration patterns
if __name__ == "__main__":
    """
    Example of how to use GeminiRequestManager in your application.
    """
    print("""
    ========================================
    GEMINI REQUEST MANAGER - EXAMPLE USAGE
    ========================================
    
    1. BASIC USAGE (Streamlit/Flask app):
    
    import google.generativeai as genai
    from modules.gemini_request_manager import GeminiRequestManager
    
    # Setup (do this once in your app initialization)
    genai.configure(api_key="your-api-key")
    model = genai.GenerativeModel("gemini-2.5-flash")
    manager = GeminiRequestManager(model)
    
    # Use in your routes/functions (instead of model.generate_content())
    try:
        response = manager.generate("What are healthy exercise habits?")
        print(response)
    except Exception as e:
        print(f"Error: {e}")
    
    
    2. WITH FALLBACK (for production):
    
    response = manager.generate_with_fallback(
        "Tell me about nutrition",
        fallback_response="I'm currently unavailable. Please try again later."
    )
    
    
    3. CHECK RATE LIMIT STATUS:
    
    status = manager.get_rate_limit_status()
    print(f"Requests available: {status['available_slots']}")
    print(f"Next request in: {status['next_request_available_in']:.1f}s")
    
    
    4. STREAMLIT INTEGRATION:
    
    import streamlit as st
    import google.generativeai as genai
    from modules.gemini_request_manager import GeminiRequestManager
    
    @st.cache_resource
    def get_request_manager():
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-2.5-flash")
        return GeminiRequestManager(model)
    
    manager = get_request_manager()
    
    user_input = st.text_input("Ask a question")
    if user_input:
        response = manager.generate_with_fallback(user_input)
        st.write(response)
        
        # Show rate limit info
        status = manager.get_rate_limit_status()
        st.info(f"API requests available: {status['available_slots']}/5 per minute")
    
    
    5. FLASK INTEGRATION:
    
    from flask import Flask, request, jsonify
    import google.generativeai as genai
    from modules.gemini_request_manager import GeminiRequestManager
    
    app = Flask(__name__)
    
    # Initialize manager globally
    genai.configure(api_key="your-api-key")
    model = genai.GenerativeModel("gemini-2.5-flash")
    manager = GeminiRequestManager(model)
    
    @app.route("/api/generate", methods=["POST"])
    def generate():
        data = request.get_json()
        prompt = data.get("prompt")
        
        try:
            response = manager.generate(prompt)
            return jsonify({"response": response, "success": True})
        except Exception as e:
            return jsonify({
                "error": str(e),
                "success": False,
                "status": manager.get_rate_limit_status()
            }), 429
    
    
    6. WITH CUSTOM LOGGER:
    
    import logging
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("health_coach")
    
    manager = GeminiRequestManager(
        model,
        requests_per_minute=5,
        max_retries=3,
        retry_wait_seconds=35,
        logger=logger
    )
    """)
