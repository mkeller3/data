CREATE TABLE accounts(
   id serial PRIMARY KEY,
   account_id text UNIQUE NOT NULL,
   venue_guests integer NOT NULL,
   venue_date TIMESTAMP NOT NULL,
   venue_name text NOT NULL,
   venue_address text NOT NULL,
   venue_latitude double precision NOT NULL,
   venue_longitude double precision NOT NULL,
   created_on TIMESTAMP NOT NULL
);

CREATE TABLE contacts(
   id serial PRIMARY KEY,
   account_id text NOT NULL,
   first_name text NOT NULL,
   last_name text NOT NULL,
   full_name text NOT NULL,
   phone_number BIGINT NOT NULL
);

CREATE TABLE groups(
   id serial PRIMARY KEY,
   account_id text UNIQUE NOT NULL,
   group_name text NOT NULL,
   contacts text NOT NULL
);

CREATE TABLE scheduled_texts(
   id serial PRIMARY KEY,
   account_id text NOT NULL,
   text_message text NOT NULL,
   group_message boolean NOT NULL,
   group_ids text,
   run_time TIMESTAMP NOT NULL
);