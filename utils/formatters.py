"""
Currency formatting utilities for PDF generation.

Provides Jinja-compatible filters for formatting currency values with
locale-specific formatting (Indian number grouping) and abbreviations.
"""

from babel.numbers import format_currency as babel_format_currency
from decimal import Decimal, ROUND_HALF_UP


def format_inr(value, style="full", currency="INR"):
    """
    Format a numeric value as Indian currency with optional abbreviations.
    
    Args:
        value: Numeric value (int, float, Decimal, or numeric string)
        style: "full" for complete formatting or "abbrev" for K/L/Cr abbreviations
        currency: ISO currency code (e.g., "INR", "USD"). Abbreviations only apply to INR.
    
    Returns:
        Formatted currency string with symbol and appropriate formatting
    
    Examples:
        format_inr(1500, "abbrev", "INR")        → "₹1.5K"
        format_inr(1500, "full", "INR")          → "₹1,500.00"
        format_inr(150000, "abbrev", "INR")      → "₹1.5L"
        format_inr(15000000, "abbrev", "INR")    → "₹1.5Cr"
        format_inr(1500, "full", "USD")          → "$1,500.00"
    """
    # Handle None, empty string, or invalid values
    if value is None or value == "" or value == "N/A":
        return "N/A"
    
    # Convert to Decimal for precise calculations
    try:
        if isinstance(value, str):
            # Remove any existing currency symbols or commas
            value = value.replace("₹", "").replace("$", "").replace(",", "").strip()
        num_value = Decimal(str(value))
    except (ValueError, TypeError):
        return "N/A"
    
    # For non-INR currencies or "full" style, use standard Babel formatting
    if currency != "INR" or style == "full":
        # Use Indian locale for INR, US locale for others
        locale = "en_IN" if currency == "INR" else "en_US"
        try:
            return babel_format_currency(num_value, currency, locale=locale)
        except Exception:
            # Fallback if Babel fails
            return f"{currency} {num_value:,.2f}"
    
    # Apply INR abbreviations for "abbrev" style
    if style == "abbrev":
        abs_value = abs(num_value)
        sign = "-" if num_value < 0 else ""
        
        # Crore: >= 1,00,00,000 (10 million)
        if abs_value >= 10000000:
            abbreviated = abs_value / 10000000
            # Round to 1 decimal place
            abbreviated = abbreviated.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
            # Remove trailing .0 if whole number
            abbreviated_str = str(abbreviated).rstrip('0').rstrip('.')
            return f"₹{sign}{abbreviated_str}Cr"
        
        # Lakh: >= 1,00,000 (100 thousand)
        elif abs_value >= 100000:
            abbreviated = abs_value / 100000
            abbreviated = abbreviated.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
            abbreviated_str = str(abbreviated).rstrip('0').rstrip('.')
            return f"₹{sign}{abbreviated_str}L"
        
        # Thousand: >= 1,000
        elif abs_value >= 1000:
            abbreviated = abs_value / 1000
            abbreviated = abbreviated.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
            abbreviated_str = str(abbreviated).rstrip('0').rstrip('.')
            return f"₹{sign}{abbreviated_str}K"
        
        # Less than 1,000: show with 2 decimals
        else:
            return f"₹{sign}{abs_value:.2f}"
    
    # Default fallback
    return babel_format_currency(num_value, currency, locale="en_IN")
