# FastAPI Backend Usage

Follow these steps to set up and run the FastAPI backend.

## 1. Create a Virtual Environment

**Linux/macOS:**
```sh
python3 -m venv venv
source venv/bin/activate
```

**Windows (Command Prompt):**
```bat
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

## 2. Install Requirements

```bash
pip install -r requirements.txt
```

## 3. Setup Environment Variables (.env)
```bash
SUPABASE_URL=YOUR_SUPABASE_URL
SUPABASE_ANON_KEY=YOUR_SUPABASE_ANON_KEY
PROJECT_URL=http://localhost:3000
PROJECT_ORIGINS=http://localhost:3000,http://localhost:3000/login,http://localhost:3000/dashboard,http://localhost:3000/simulation,http://localhost:3000/simulation/stack,http://localhost:3000/simulation/queue,http://localhost:3000/simulation/binary-tree,http://localhost:3000/simulation/binary-search-tree,http://localhost:3000/simulation/hanoi-tower,http://localhost:3000/factorial,http://localhost:3000/fibonacci,http://localhost:3000/logs,http://localhost:3000/faqs
API_URL=http://localhost:8000/api
SUPABASE_SERVICE_ROLE_KEY=SUPABASE_SERVICE_ROLE_KEY
OPEN_ROUTER_API_KEY=YOUR_OPEN_ROUTER_KEY
```

## 3. Run the FastAPI Development Server

```bash
fastapi dev app/server.py
```

## NOTE
```
    - Unit tests are outdated, may not work
```

---

## DATABASE Schema (SQL)
```bash
-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.history (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  page text,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  user_id uuid NOT NULL,
  updated_at timestamp with time zone DEFAULT now(),
  seconds_spent double precision DEFAULT '0'::double precision,
  CONSTRAINT history_pkey PRIMARY KEY (id),
  CONSTRAINT activity_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.profile(id)
);
CREATE TABLE public.profile (
  id uuid NOT NULL,
  username text UNIQUE,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  monthly_messages ARRAY DEFAULT '{}'::text[],
  email text DEFAULT ''::text,
  CONSTRAINT profile_pkey PRIMARY KEY (id),
  CONSTRAINT profiles_id_fkey FOREIGN KEY (id) REFERENCES auth.users(id)
);
CREATE TABLE public.settings (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  theme text DEFAULT 'dark'::text,
  speed double precision DEFAULT '0.25'::double precision,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  user_id uuid DEFAULT gen_random_uuid(),
  CONSTRAINT settings_pkey PRIMARY KEY (id),
  CONSTRAINT settings_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.profile(id)
);
CREATE TABLE public.simulation (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL UNIQUE,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  type text NOT NULL,
  status text NOT NULL,
  total_visits bigint NOT NULL DEFAULT '0'::bigint,
  last_visit_at timestamp with time zone,
  completed_at timestamp with time zone,
  user_id uuid NOT NULL,
  seconds_spent double precision DEFAULT '0'::double precision,
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT simulation_pkey PRIMARY KEY (id),
  CONSTRAINT simulation_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.profile(id)
);
CREATE TABLE public.stats (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  user_id uuid NOT NULL,
  current_streak bigint DEFAULT '0'::bigint,
  longest_streak bigint DEFAULT '0'::bigint,
  seconds_spent double precision,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT stats_pkey PRIMARY KEY (id),
  CONSTRAINT statistics_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.profile(id)
);
```


The backend will be available at http://localhost:8000.


