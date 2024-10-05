# 🥊 FightLive v1.0.0

Stay updated with the latest UFC fight results and scorecards directly in your Discord server! 

FightLive is a streamlined tool that fetches live updates from UFCNews and delivers them in an engaging format using Discord webhooks.


<img width="559" alt="Screenshot 2024-10-05 at 1 20 29 AM" src="https://github.com/user-attachments/assets/7e012935-27ba-4192-a623-2824b9baa4c1">


## Installation

#### make sure to set up venv before you install the dependencies
1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/ufc-fight-tracker.git
   cd ufc-fight-tracker
   ```

2. **Set Up Environment Variables**
   
   Create a `.env` file in the root directory and add the following:
   ```
   WEBHOOK_URL=your_discord_webhook_url
   AUTH_TOKEN=your_twitter_auth_token
   X_ACCOUNT=official_ufc_account
   POSTGRES_USER=your_db_user
   POSTGRES_PASSWORD=your_db_password
   POSTGRES_DB=ufc_fight_tracker
   DATABASE_URL=postgresql://your_db_user:your_db_password@db:5432/ufc_fight_tracker
   ```
3. **Install dependencies**
   ```bash  
   pip3 install -r requirements.txt
   ```
4. **Setup migration files**
   ```bash
   alembic upgrade head
   ```
5. **Start Docker Services**
   ```bash
   docker-compose up -d
   ```
6. **Run Program**
   ```bash
   python3 run.py
   ```
### Tests

1. **Run pytest**
   
   ```bash
   pytest tests/FILENAME.py
   ```
##  Contributing

We welcome contributions from the community! If you're passionate about UFC and coding, consider contributing to this project.

1. **Fork the Repository**
2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/YourFeature
   ```
3. **Commit Your Changes**
   ```bash
   git commit -m "Add some feature"
   ```
4. **Push to the Branch**
   ```bash
   git push origin feature/YourFeature
   ```
5. **Open a Pull Request**

