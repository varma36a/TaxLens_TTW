# TaxLens_TTW

## Local Setup

Run the backend and frontend in separate terminal windows.

## Backend

The backend is a FastAPI app located in `TaxLens/backend`.

1. Go to the backend folder:

   ```bash
   cd TaxLens/backend
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create the local environment file:

   ```bash
   cp .env.example .env
   ```

   Update `.env` with your Azure OpenAI values if you want to use AI explanation features. Keep `MONGODB_URI=mongodb://localhost:27017` and `DATABASE_NAME=taxlens` for the default local MongoDB setup.

5. Start MongoDB locally. For example, with Homebrew on macOS:

   ```bash
   brew services start mongodb-community
   ```

6. Start the backend server:

   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

   The API will be available at `http://127.0.0.1:8000`.

## Frontend

The frontend is an Angular app located in `TaxLens/frontend/taxlens-widget`.

1. Go to the frontend folder:

   ```bash
   cd TaxLens/frontend/taxlens-widget
   ```

2. Install Node dependencies:

   ```bash
   npm install
   ```

3. Start the Angular development server:

   ```bash
   npm start
   ```

4. Open the app in your browser:

   ```text
   http://localhost:4200
   ```

The frontend is configured to call the backend at `http://127.0.0.1:8000`, so start the backend before using upload, compare, scenario, or chat features.
