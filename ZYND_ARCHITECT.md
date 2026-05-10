# 🧠 Member 2: The Agent Architect
**Mission:** AI Decision Engine & Content Creation

## 📋 Overview
The Agent Architect manages the "brain" of the operation. This role takes raw competitor data and uses Zynd AI logic to apply a 5% competitive discount and generate high-end product photography.

## 🚀 Implementation Strategy
- **Pricing Logic:** A strictly enforced business rule to undercut competitors by exactly 5%, calculated dynamically.
- **AI Image Vault:** Integrates with the Pollinations AI engine to generate professional studio-grade photography for every product discovered.
- **Persistence Layer:** Unlike standard AI wrappers, the Architect downloads and saves these images locally to `src/frontend/assets/images/` for permanent storage.
- **Security:** Handles asymmetric `keypair.json` authentication and secure environment variable loading.

## 📂 Key Outputs
- `src/scripts/zynd_agent.py`: The AI and pricing logic processor.
- `store_data.json`: The final database used by the frontend.
