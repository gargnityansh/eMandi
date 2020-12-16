--GAME TABLE

CREATE TABLE public.game
(
    game_name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    date_of_release date NOT NULL,
    game_size numeric(4,1) NOT NULL,
    prod_studio character varying(30) COLLATE pg_catalog."default" NOT NULL,
    mrp numeric(6,2) NOT NULL,
    game_link text COLLATE pg_catalog."default" NOT NULL,
    image text COLLATE pg_catalog."default",
    description text COLLATE pg_catalog."default",
    curr_version character varying(10) COLLATE pg_catalog."default" NOT NULL,
    update_link text COLLATE pg_catalog."default",
    date_of_update date,
    username character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT game_pkey PRIMARY KEY (game_name, date_of_release),
    CONSTRAINT game_username_fkey FOREIGN KEY (username)
        REFERENCES public.user_details (username) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE SET NULL
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.game
    OWNER to postgres;

--USER DETAILS TABLE

CREATE TABLE public.user_details
(
    username character varying(20) COLLATE pg_catalog."default" NOT NULL,
    fname character varying(15) COLLATE pg_catalog."default",
    lname character varying(15) COLLATE pg_catalog."default",
    phno character(10) COLLATE pg_catalog."default",
    emailid character varying(40) COLLATE pg_catalog."default" NOT NULL,
    password character varying COLLATE pg_catalog."default" NOT NULL,
    "isClient" boolean NOT NULL DEFAULT false,
    CONSTRAINT user_details_pkey PRIMARY KEY (username)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.user_details
    OWNER to postgres;

--IDENTTY TABLE

CREATE TABLE public.identty
(
    game_name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    date_of_release date NOT NULL,
    gameid character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT identty_pkey PRIMARY KEY (gameid),
    CONSTRAINT identty_gamename_fkey FOREIGN KEY (date_of_release, game_name)
        REFERENCES public.game (date_of_release, game_name) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.identty
    OWNER to postgres;

--CATEGORY TABLE

CREATE TABLE public.category
(
    gameid character varying COLLATE pg_catalog."default" NOT NULL,
    cat_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT category_pkey PRIMARY KEY (gameid, cat_name),
    CONSTRAINT category_gameid_fkey FOREIGN KEY (gameid)
        REFERENCES public.identty (gameid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.category
    OWNER to postgres;

--TRANSACTIONS TABLE

CREATE TABLE public.transactions
(
    gameid character varying COLLATE pg_catalog."default" NOT NULL,
    username character varying(20) COLLATE pg_catalog."default" NOT NULL,
    selling_date date NOT NULL,
    price numeric(6,2) NOT NULL,
    curr_version character varying(10) COLLATE pg_catalog."default",
    paymentopt character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT transactions_pkey PRIMARY KEY (gameid, username),
    CONSTRAINT transaction_gameid_fkey FOREIGN KEY (gameid)
        REFERENCES public.identty (gameid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE SET NULL,
    CONSTRAINT transaction_username_fkey FOREIGN KEY (username)
        REFERENCES public.user_details (username) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.transactions
    OWNER to postgres;

--RATE REVIEW TABLE

CREATE TABLE public.ratereview
(
    gameid character varying COLLATE pg_catalog."default" NOT NULL,
    username character varying(20) COLLATE pg_catalog."default" NOT NULL,
    rating numeric(1,0),
    reviewtext text COLLATE pg_catalog."default",
    CONSTRAINT ratereview_pkey PRIMARY KEY (gameid, username),
    CONSTRAINT ratereview_gameid_fkey FOREIGN KEY (gameid)
        REFERENCES public.identty (gameid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT ratereview_username_fkey FOREIGN KEY (username)
        REFERENCES public.user_details (username) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.ratereview
    OWNER to postgres;