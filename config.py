import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SUPABASE_URL = "https://vdwnvbbjbueaqpvsgirj.supabase.co"      # Project URL
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZkd252YmJqYnVlYXFwdnNnaXJqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDYzNzMyMjAsImV4cCI6MjA2MTk0OTIyMH0.CL1mr6u7Rs85MRZJq6U1IBiNeRN-OKOAJARpLVxcbKk" #Key
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')