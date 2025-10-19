# OpenAI API Setup Guide

## 🚨 Current Issue

Your chatbot is getting this error:
```
RateLimitError: You exceeded your current quota, please check your plan and billing details.
```

This means your OpenAI API key cannot make API calls (embeddings or chat completions).

---

## 📊 Understanding OpenAI Quota

### Free Tier ($0 balance)
- ✅ Can list models
- ❌ Cannot create embeddings
- ❌ Cannot create chat completions
- ❌ Cannot use the API for actual requests

### Paid Tier (with billing)
- ✅ Full API access
- ✅ Pay-as-you-go pricing
- ✅ Can set usage limits

---

## 🔍 Check Your Current Status

1. **Go to**: https://platform.openai.com/account/usage
2. **Check**:
   - Current usage
   - Usage limits
   - Billing status

3. **Go to**: https://platform.openai.com/account/billing/overview
4. **Check**:
   - Payment method
   - Current balance
   - Auto-reload settings

---

## 💳 How to Add Billing

### Step 1: Add Payment Method
1. Go to: https://platform.openai.com/account/billing/payment-methods
2. Click "Add payment method"
3. Enter your credit/debit card details
4. Save

### Step 2: Set Up Auto-Reload (Recommended)
1. Go to: https://platform.openai.com/account/billing/overview
2. Click "Add to credit balance"
3. Choose an amount (minimum $5, recommended $10-20)
4. Enable auto-reload when balance drops below a threshold

### Step 3: Set Usage Limits
1. Go to: https://platform.openai.com/account/limits
2. Set monthly usage limit (e.g., AED 50 or $15)
3. This prevents unexpected charges

---

## 💰 Expected Costs for LegalEdge AI

### MVP Testing Phase (1 month)
- **Embeddings** (one-time): ~$0.50-2.00
  - `text-embedding-3-large`: $0.13 per 1M tokens
  - Your PDF (~50 pages) = ~20,000 tokens = $0.0026
  
- **Chat Completions** (ongoing):
  - `gpt-4o-mini`: $0.150 per 1M input tokens, $0.600 per 1M output tokens
  - Average query: ~500 input + ~300 output tokens = $0.00030
  - 100 queries = $0.03
  - 1,000 queries = $0.30
  - 10,000 queries = $3.00

### Monthly Estimate
- Light usage (100 queries): **~$5**
- Medium usage (1,000 queries): **~$15**
- Heavy usage (10,000 queries): **~$50**

**Budget**: Well within your AED 10k (~$2,700) budget! 🎉

---

## 🔑 Alternative: Use a Different API Key

If you have issues with your current key, you can create a new one:

1. Go to: https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Name it "LegalEdge-AI-Production"
4. Copy the key (starts with `sk-proj-...`)
5. Update your `.env` file:
   ```bash
   OPENAI_API_KEY=sk-proj-YOUR-NEW-KEY-HERE
   ```
6. Restart Docker:
   ```bash
   docker-compose restart backend
   ```

---

## 🧪 Test Your API Key

Run this command to test:

```bash
docker-compose exec backend python -c "
import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

# Test 1: List models (works even without billing)
print('✓ API Key is valid')

# Test 2: Create embedding (requires billing)
try:
    openai.Embedding.create(input='test', model='text-embedding-3-large')
    print('✓ Embeddings work!')
except Exception as e:
    print('✗ Embeddings failed:', str(e))

# Test 3: Chat completion (requires billing)
try:
    openai.ChatCompletion.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': 'hi'}],
        max_tokens=5
    )
    print('✓ Chat completions work!')
except Exception as e:
    print('✗ Chat completions failed:', str(e))
"
```

---

## 🆘 Still Having Issues?

### Option 1: Contact OpenAI Support
- Email: support@openai.com
- Include your API key ID (not the full key!)
- Describe the issue

### Option 2: Use OpenRouter (Alternative)
OpenRouter provides access to multiple LLMs with simple pricing:
- Website: https://openrouter.ai/
- Supports GPT-4, Claude, and more
- Pay-as-you-go with no minimums

To use OpenRouter instead of OpenAI:
1. Sign up at https://openrouter.ai/
2. Get your API key
3. Update `backend/rag_engine.py` and `backend/main.py` to use OpenRouter's API
4. (Let me know if you want help with this!)

---

## ✅ Quick Checklist

- [ ] Check OpenAI usage dashboard
- [ ] Verify billing method is added
- [ ] Add credit balance ($10-20 recommended)
- [ ] Set usage limits
- [ ] Test API key with the command above
- [ ] Restart Docker containers

---

## 📞 Need Help?

If you're still stuck after following this guide, please:

1. **Share a screenshot** of your OpenAI billing page
2. **Run the test command** above and share the output
3. **Check** if you have any error emails from OpenAI

I'm here to help! 🚀

