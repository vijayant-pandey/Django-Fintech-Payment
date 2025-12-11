from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
import requests
from decimal import Decimal, InvalidOperation
import logging
logger = logging.getLogger(__name__)

def api_convert(request):
    """
    Robust converter endpoint.
    GET params: ?from=USD&to=AUD&amount=100
    """
    frm = (request.GET.get("from", "USD") or "USD").upper()
    to = (request.GET.get("to", "USD") or "USD").upper()
    amount = request.GET.get("amount", "1")



    cache_key = f"fx_rate_{frm}_{to}"
    cached = cache.get(cache_key)
    if cached:
        try:
            rate = Decimal(cached)
        except InvalidOperation:
            # clear bad cache and continue to fetch
            cache.delete(cache_key)
            cached = None

    if not cached:
        # Try primary endpoint: /convert with amount=1 (so result == rate)
        try:
            url = f"https://api.frankfurter.app/latest?from={frm}&to={to}"
            resp = requests.get(url, timeout=6)
            resp.raise_for_status()
            j = resp.json()

            # frankfurter returns {"amount":1,"base":"USD","date":"YYYY-MM-DD","rates":{"AUD":1.45}}
            rates = j.get("rates") or {}
            rate_val = rates.get(to)


        except Exception as e:
            logger.exception("Frankfurter primary call failed")
            # return JsonResponse({"error": "rate_fetch_failed", "detail": str(e)}, status=502)
            rate_val = None

        # Prefer info.rate, fallback to result
        # rate_val = None
        # try:
        #     rate_val = j.get("info", {}).get("rate")
        # except Exception:
        #     rate_val = None

        # if rate_val is None:
        #     # fallback to 'result' (when amount=1, result is the rate)
        #     rate_val = j.get("result")

        # final fallback: call /latest to get rates dict
        if rate_val is None:
            try:
                url2 = f"https://api.exchangerate.host/convert?from={frm}&to={to}&amount=1"
                resp2 = requests.get(url2, timeout=6)
                resp2.raise_for_status()
                j2 = resp2.json()
                # rates = j2.get("rates") or {}
                rate_val = j2.get("info", {}).get("rate") or j2.get("result")
            except Exception as e:
                logger.exception("Fallback exchangerate.host call failed")
                # return JsonResponse({"error": "rate_fetch_failed", "detail": "primary and fallback endpoints failed", "detail2": str(e)}, status=502)
                rate_val = None

        # Validate rate_val
        if rate_val is None:
            logger.error("Rate missing from APIs. frankfurter response: %s", j if 'j' in locals() else None)
            return JsonResponse({
                "error": "rate_missing", 
                "detail": "no rate in API response", 
                "frankfurter_response": j if 'j' in locals() else None
                }, status=502)

        # Convert to Decimal safely
        try:
            rate = Decimal(str(rate_val))
        except (InvalidOperation, TypeError, ValueError) as e:
            logger.exception("Invalid rate value from API: %r", rate_val)
            return JsonResponse({"error": "invalid_rate", "detail": str(e), "rate_value": rate_val, "api_response": j}, status=502)

        # Cache string representation
        cache.set(cache_key, str(rate), 300)

    # Parse amount
    try:
        amt = Decimal(str(amount))
    except (InvalidOperation, TypeError, ValueError) as e:
        return JsonResponse({"error": "invalid_amount", "detail": str(e)}, status=400)

    converted = (rate * amt).quantize(Decimal("0.01"))
    return JsonResponse({"rate": str(rate), "converted": str(converted)})


# Create your views here.
def index(request):
    return render(request, "core/index.html")

def contact(request):
    return render(request, "core/contact.html")

def about(request):
    return render(request, "core/about.html")


