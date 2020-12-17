--
-- PostgreSQL database dump
--

-- Dumped from database version 13.1
-- Dumped by pg_dump version 13.1

-- Started on 2020-12-17 20:29:46

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3085 (class 1262 OID 17487)
-- Name: Game; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE "Game" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'English_India.1252';


ALTER DATABASE "Game" OWNER TO postgres;

\connect "Game"

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2 (class 3079 OID 17533)
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- TOC entry 3086 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


--
-- TOC entry 259 (class 1255 OID 17659)
-- Name: autoInsert_identty(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public."autoInsert_identty"() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
INSERT INTO public.identty(
	game_name, date_of_release, gameid)
	VALUES (NEW.game_name, NEW.date_of_release,
			concat_ws('_', NEW.game_name, NEW.date_of_release :: character varying));
RETURN NEW;
END;
$$;


ALTER FUNCTION public."autoInsert_identty"() OWNER TO postgres;

--
-- TOC entry 258 (class 1255 OID 17658)
-- Name: noReleases_in_future(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public."noReleases_in_future"() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN

IF ( NEW.date_of_release ::date > (SELECT CURRENT_DATE +1)) THEN
RAISE EXCEPTION 'You cannot add games in the future';
END IF;
RETURN NEW;
END;
$$;


ALTER FUNCTION public."noReleases_in_future"() OWNER TO postgres;

--
-- TOC entry 257 (class 1255 OID 17657)
-- Name: noSales_in_future(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public."noSales_in_future"() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
IF ( NEW.selling_date ::date > (SELECT CURRENT_DATE +1)) THEN
RAISE EXCEPTION 'You cannot buy games in the future';
END IF;
RETURN NEW;
END;
$$;


ALTER FUNCTION public."noSales_in_future"() OWNER TO postgres;

--
-- TOC entry 256 (class 1255 OID 17656)
-- Name: password_limit(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.password_limit() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
IF (SELECT LENGTH(NEW.password) < '6') THEN
RAISE EXCEPTION 'Please enter a 6 digit password, with no trailing spaces';
END IF;
RETURN NEW;
END;
$$;


ALTER FUNCTION public.password_limit() OWNER TO postgres;

--
-- TOC entry 260 (class 1255 OID 17676)
-- Name: phno_limit(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.phno_limit() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
IF (SELECT LENGTH(NEW.phno) <> '10') THEN
RAISE EXCEPTION 'Please enter a valid phone number';
END IF;
RETURN NEW;
END;
$$;


ALTER FUNCTION public.phno_limit() OWNER TO postgres;

--
-- TOC entry 255 (class 1255 OID 17655)
-- Name: sell_after_release(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.sell_after_release() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
IF (NEW.selling_date:: date <(SELECT date_of_release from game 
							  where game_name = (SELECT game_name from identty
												 where gameid = NEW.gameid)
							  and date_of_release = (SELECT date_of_release from identty
													 where gameid = NEW.gameid)):: date)
THEN
RAISE EXCEPTION 'You cannot pre-order the game';
END IF;
RETURN NEW;
END;
$$;


ALTER FUNCTION public.sell_after_release() OWNER TO postgres;

--
-- TOC entry 254 (class 1255 OID 17654)
-- Name: update_after_release(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.update_after_release() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
IF (NEW.date_of_update :: date < NEW.date_of_release :: date) THEN
RAISE EXCEPTION 'date_of_update should be after date_of_release';
END IF;
RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_after_release() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 204 (class 1259 OID 17605)
-- Name: category; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.category (
    gameid character varying NOT NULL,
    cat_name character varying(20) NOT NULL
);


ALTER TABLE public.category OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 17579)
-- Name: game; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.game (
    game_name character varying(50) NOT NULL,
    date_of_release date NOT NULL,
    game_size numeric(4,1) NOT NULL,
    prod_studio character varying(30) NOT NULL,
    mrp numeric(6,2) NOT NULL,
    game_link text NOT NULL,
    image text,
    description text,
    curr_version character varying(10) NOT NULL,
    update_link text,
    username character varying(20) NOT NULL
);


ALTER TABLE public.game OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 17592)
-- Name: identty; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.identty (
    game_name character varying(50) NOT NULL,
    date_of_release date NOT NULL,
    gameid character varying NOT NULL
);


ALTER TABLE public.identty OWNER TO postgres;

--
-- TOC entry 206 (class 1259 OID 17636)
-- Name: ratereview; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ratereview (
    gameid character varying NOT NULL,
    username character varying(20) NOT NULL,
    rating numeric(1,0),
    reviewtext text
);


ALTER TABLE public.ratereview OWNER TO postgres;

--
-- TOC entry 205 (class 1259 OID 17618)
-- Name: transactions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.transactions (
    gameid character varying NOT NULL,
    username character varying(20) NOT NULL,
    selling_date date NOT NULL,
    price numeric(6,2) NOT NULL,
    curr_version character varying(10),
    order_id character varying NOT NULL
);


ALTER TABLE public.transactions OWNER TO postgres;

--
-- TOC entry 201 (class 1259 OID 17570)
-- Name: user_details; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_details (
    username character varying(20) NOT NULL,
    fname character varying(15),
    lname character varying(15),
    phno character(10),
    emailid character varying(40) NOT NULL,
    password character varying NOT NULL,
    "isClient" boolean DEFAULT false NOT NULL
);


ALTER TABLE public.user_details OWNER TO postgres;

--
-- TOC entry 3077 (class 0 OID 17605)
-- Dependencies: 204
-- Data for Name: category; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.category (gameid, cat_name) VALUES ('Cyberpunk 2077_2020-12-01', 'FPS');
INSERT INTO public.category (gameid, cat_name) VALUES ('Red Dead Online_2020-12-02', 'Open World');
INSERT INTO public.category (gameid, cat_name) VALUES ('Project Wingman_2020-12-01', 'Simulation');
INSERT INTO public.category (gameid, cat_name) VALUES ('Phasmophobia_2020-09-18', 'Horror');
INSERT INTO public.category (gameid, cat_name) VALUES ('Dead by Daylight_2016-12-01', 'Horror');
INSERT INTO public.category (gameid, cat_name) VALUES ('Among Us_2018-11-16', 'Casual');
INSERT INTO public.category (gameid, cat_name) VALUES ('Satisfactory_2020-06-08', 'Simulation');
INSERT INTO public.category (gameid, cat_name) VALUES ('Fall Guys: Ultimate Knockout_2020-08-04', 'Casual');
INSERT INTO public.category (gameid, cat_name) VALUES ('Among Us_2018-11-16', 'Open World');
INSERT INTO public.category (gameid, cat_name) VALUES ('Among Us_2018-11-16', 'Action');
INSERT INTO public.category (gameid, cat_name) VALUES ('GTA 5_2015-04-14', 'Open World');
INSERT INTO public.category (gameid, cat_name) VALUES ('GTA 5_2015-04-14', ' Action');
INSERT INTO public.category (gameid, cat_name) VALUES ('Mario_2020-12-16', 'Casual');


--
-- TOC entry 3075 (class 0 OID 17579)
-- Dependencies: 202
-- Data for Name: game; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.game (game_name, date_of_release, game_size, prod_studio, mrp, game_link, image, description, curr_version, update_link, username) VALUES ('Cyberpunk 2077', '2020-12-01', 70.0, 'CD PROJEKT RED', 2999.00, 'https://cdn-fastly.obsproject.com/downloads/OBS-Studio-26.0.2-Full-Installer-x64.exe', 'https://images.indianexpress.com/2020/11/cyberpunk2077.jpg', 'Cyberpunk 2077 is an open-world, action-adventure story set in Night City, a megalopolis obsessed with power, glamour and body modification. You play as V, a mercenary outlaw going after a one-of-a-kind implant that is the key to immortality.', '1.0.0', NULL, 'ab');
INSERT INTO public.game (game_name, date_of_release, game_size, prod_studio, mrp, game_link, image, description, curr_version, update_link, username) VALUES ('Among Us', '2018-11-16', 0.3, 'Innersloth', 129.00, 'https://cdn-fastly.obsproject.com/downloads/OBS-Studio-26.0.2-Full-Installer-x64.exe', 'https://cdn.cloudflare.steamstatic.com/steam/apps/945360/ss_649e19ff657fa518d4c2b45bed7ffdc4264a4b3a.1920x1080.jpg?t=1606422465', 'An online and local party game of teamwork and betrayal for 4-10 players...in space!', '5', NULL, 'ab');
INSERT INTO public.game (game_name, date_of_release, game_size, prod_studio, mrp, game_link, image, description, curr_version, update_link, username) VALUES ('Satisfactory', '2020-06-08', 15.0, 'Coffee Stain Studios', 749.00, 'https://cdn-fastly.obsproject.com/downloads/OBS-Studio-26.0.2-Full-Installer-x64.exe', 'https://cdn.cloudflare.steamstatic.com/steam/apps/526870/ss_dcb79211f2f9bac1e6a2d85aad132fc3ae909001.1920x1080.jpg?t=1598908784', 'Satisfactory is a first-person open-world factory building game with a dash of exploration and combat. Play alone or with friends, explore an alien planet, create multi-story factories, and enter conveyor belt heaven!', '1.0.0', NULL, 'ab');
INSERT INTO public.game (game_name, date_of_release, game_size, prod_studio, mrp, game_link, image, description, curr_version, update_link, username) VALUES ('Fall Guys: Ultimate Knockout', '2020-08-04', 2.0, 'Mediatonic', 529.00, 'https://cdn-fastly.obsproject.com/downloads/OBS-Studio-26.0.2-Full-Installer-x64.exe', 'https://cdn.cloudflare.steamstatic.com/steam/apps/1097150/ss_a0758d69b45b016a386761e1415f2227542c27be.1920x1080.jpg?t=1606255678', 'Fall Guys is a massively multiplayer party game with up to 60 players online in a free-for-all struggle through round after round of escalating chaos until one victor remains!', '2.0', NULL, 'ab');
INSERT INTO public.game (game_name, date_of_release, game_size, prod_studio, mrp, game_link, image, description, curr_version, update_link, username) VALUES ('Dead by Daylight', '2016-12-01', 25.0, 'Behaviour Interactive Inc.', 569.00, 'https://cdn-fastly.obsproject.com/downloads/OBS-Studio-26.0.2-Full-Installer-x64.exe', 'https://cdn.cloudflare.steamstatic.com/steam/apps/1474030/ss_f31c9951bb396c3b1f4a3d177519b9472bb9e886.1920x1080.jpg?t=1606861292', 'Dead by Daylight is a multiplayer (4vs1) horror game where one player takes on the role of the savage Killer, and the other four players play as Survivors, trying to escape the Killer and avoid being caught and killed.', '12', NULL, 'admin');
INSERT INTO public.game (game_name, date_of_release, game_size, prod_studio, mrp, game_link, image, description, curr_version, update_link, username) VALUES ('Red Dead Online', '2020-12-02', 150.0, 'Rockstar Games', 375.00, 'https://cdn-fastly.obsproject.com/downloads/OBS-Studio-26.0.2-Full-Installer-x64.exe', 'https://cdn.cloudflare.steamstatic.com/steam/apps/1404210/ss_11910cbe7b91268b17351baf2720af4f39395c08.1920x1080.jpg?t=1606871612', 'Step into the vibrant, ever-evolving world of Red Dead Online and experience life in frontier America. Chase down bounties, battle outlaw gangs and other players, hunt, fish and trade, search for exotic treasures, run Moonshine, and much more to discover in a world of astounding depth and detail.', '4.6.8', 'https://discord.com/api/download?platform=win', 'ab');
INSERT INTO public.game (game_name, date_of_release, game_size, prod_studio, mrp, game_link, image, description, curr_version, update_link, username) VALUES ('GTA 5', '2015-04-14', 72.0, 'Rockstar', 2099.00, 'https://cdn-fastly.obsproject.com/downloads/OBS-Studio-26.0.2-Full-Installer-x64.exe', 'https://i.pinimg.com/originals/0b/07/14/0b0714cfb3ad2ba9960f4b38b37a9de1.jpg', 'Grand Theft Auto V for PC offers players the option to explore the award-winning world of Los Santos and Blaine County in resolutions of up to 4k and beyond, as well as the chance to experience the game running at 60 frames per second.', 'GTA 5', NULL, 'admin');
INSERT INTO public.game (game_name, date_of_release, game_size, prod_studio, mrp, game_link, image, description, curr_version, update_link, username) VALUES ('Mario', '2020-12-16', 0.7, 'Nintendo', 80.45, 'https://cdn-fastly.obsproject.com/downloads/OBS-Studio-26.0.2-Full-Installer-x64.exe', 'https://c.files.bbci.co.uk/F98B/production/_99838836_mario976.jpg', 'Super Mario is a platform game series created by Nintendo, featuring their mascot, Mario. Alternatively called the Super Mario Bros. series or simply the Mario series, it is the central series of the greater Mario franchise. At least one Super Mario game has been released for every major Nintendo video game console.', 'Mario', NULL, 'ab');
INSERT INTO public.game (game_name, date_of_release, game_size, prod_studio, mrp, game_link, image, description, curr_version, update_link, username) VALUES ('Phasmophobia', '2020-09-18', 15.0, 'Kinetic Games', 439.00, 'https://discord.com/api/download?platform=win', 'https://cdn.cloudflare.steamstatic.com/steam/apps/739630/ss_59023d418d1825e574ad75911da34f5814a6bb9d.1920x1080.jpg?t=1606429609', 'Phasmophobia is a 4 player online co-op psychological horror. Paranormal activity is on the rise and it’s up to you and your team to use all the ghost hunting equipment at your disposal in order to gather as much evidence as you can.', '3.2.5', NULL, 'ab');
INSERT INTO public.game (game_name, date_of_release, game_size, prod_studio, mrp, game_link, image, description, curr_version, update_link, username) VALUES ('Project Wingman', '2020-12-01', 16.0, 'Sector D2', 569.00, 'https://discord.com/api/download?platform=win', 'https://cdn.cloudflare.steamstatic.com/steam/apps/895870/ss_a198aed40e8109bc44144a7aa693fc167d2b7487.1920x1080.jpg?t=1606868166', 'Project Wingman is a flight action game that lets you take the seat of advanced fighter jets and become a true ace. Fight in various missions and gamemodes ranging from intense aerial dogfights to large scale ground assault in an alternate scorched earth setting.', '5.4.2', 'https://cdn-fastly.obsproject.com/downloads/OBS-Studio-26.0.2-Full-Installer-x64.exe', 'admin');


--
-- TOC entry 3076 (class 0 OID 17592)
-- Dependencies: 203
-- Data for Name: identty; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.identty (game_name, date_of_release, gameid) VALUES ('Cyberpunk 2077', '2020-12-01', 'Cyberpunk 2077_2020-12-01');
INSERT INTO public.identty (game_name, date_of_release, gameid) VALUES ('Red Dead Online', '2020-12-02', 'Red Dead Online_2020-12-02');
INSERT INTO public.identty (game_name, date_of_release, gameid) VALUES ('Project Wingman', '2020-12-01', 'Project Wingman_2020-12-01');
INSERT INTO public.identty (game_name, date_of_release, gameid) VALUES ('Phasmophobia', '2020-09-18', 'Phasmophobia_2020-09-18');
INSERT INTO public.identty (game_name, date_of_release, gameid) VALUES ('Dead by Daylight', '2016-12-01', 'Dead by Daylight_2016-12-01');
INSERT INTO public.identty (game_name, date_of_release, gameid) VALUES ('Among Us', '2018-11-16', 'Among Us_2018-11-16');
INSERT INTO public.identty (game_name, date_of_release, gameid) VALUES ('Satisfactory', '2020-06-08', 'Satisfactory_2020-06-08');
INSERT INTO public.identty (game_name, date_of_release, gameid) VALUES ('Fall Guys: Ultimate Knockout', '2020-08-04', 'Fall Guys: Ultimate Knockout_2020-08-04');
INSERT INTO public.identty (game_name, date_of_release, gameid) VALUES ('GTA 5', '2015-04-14', 'GTA 5_2015-04-14');
INSERT INTO public.identty (game_name, date_of_release, gameid) VALUES ('Mario', '2020-12-16', 'Mario_2020-12-16');


--
-- TOC entry 3079 (class 0 OID 17636)
-- Dependencies: 206
-- Data for Name: ratereview; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3078 (class 0 OID 17618)
-- Dependencies: 205
-- Data for Name: transactions; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.transactions (gameid, username, selling_date, price, curr_version, order_id) VALUES ('Project Wingman_2020-12-01', 'ab', '2020-12-16', 569.00, '1.0.2', 'order_GDlU7CsOqF7sep');
INSERT INTO public.transactions (gameid, username, selling_date, price, curr_version, order_id) VALUES ('GTA 5_2015-04-14', 'ab', '2020-12-16', 2099.00, 'GTA 5', 'order_GDmqj6Nxqcstim');
INSERT INTO public.transactions (gameid, username, selling_date, price, curr_version, order_id) VALUES ('Cyberpunk 2077_2020-12-01', 'howdy', '2020-12-16', 2999.00, '1.0.0', 'order_GDn62af2DwdnvM');
INSERT INTO public.transactions (gameid, username, selling_date, price, curr_version, order_id) VALUES ('Satisfactory_2020-06-08', 'howdy', '2020-12-16', 749.00, '1.0.0', 'order_GDn7kTGMYJG06S');
INSERT INTO public.transactions (gameid, username, selling_date, price, curr_version, order_id) VALUES ('Project Wingman_2020-12-01', 'ayush', '2020-12-16', 569.00, '1.0.2', 'order_GDnCpgbq8tnjFV');
INSERT INTO public.transactions (gameid, username, selling_date, price, curr_version, order_id) VALUES ('Red Dead Online_2020-12-02', 'dev', '2020-12-16', 375.00, '1.0.1', 'order_GDnhcy8HzsIbpv');
INSERT INTO public.transactions (gameid, username, selling_date, price, curr_version, order_id) VALUES ('Satisfactory_2020-06-08', 'dev', '2020-12-16', 749.00, '1.0.0', 'order_GDnixOihW0FhYH');


--
-- TOC entry 3074 (class 0 OID 17570)
-- Dependencies: 201
-- Data for Name: user_details; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.user_details (username, fname, lname, phno, emailid, password, "isClient") VALUES ('abc', 'a', 'bc', '1234567890', 'abc@gmail.com', '$2a$06$0I3a9SLUYMdAPDdtUUaf7uQJccFqoq5rilP8pWvvXBTsMxolX43Oa', false);
INSERT INTO public.user_details (username, fname, lname, phno, emailid, password, "isClient") VALUES ('abd', 'a', 'bd', '1234567890', 'abd@gmail.com', '$2a$06$1L/6RbYsOftNpzIt5Duqb.mxpP5buD9hVNicYWGmVhUQMwocJvK6a', false);
INSERT INTO public.user_details (username, fname, lname, phno, emailid, password, "isClient") VALUES ('abe', 'a', 'be', '1234567890', 'abe@gmail.com', '$2a$06$Kj2BMFDsPPkOG/iL91rmneEn78JktviwqEaVTZV6dvIHMuZzsJcmC', false);
INSERT INTO public.user_details (username, fname, lname, phno, emailid, password, "isClient") VALUES ('howdy', 'how', 'dy', '4567894561', 'howdy@gmail.com', '$2a$06$.UvyA42mNdibhpuUcRGgDey1sdsnKc0JIceC.DQDtCbfTAbQCA8Y.', false);
INSERT INTO public.user_details (username, fname, lname, phno, emailid, password, "isClient") VALUES ('ayush', 'ayush', 'pawar', '7894561231', 'stist123456789@gmail.com', '$2a$06$R0G4YCuzrJxKpxcYoir.lOKpyD.GEC2ygjZ8WotLCs00GhCduvI5a', false);
INSERT INTO public.user_details (username, fname, lname, phno, emailid, password, "isClient") VALUES ('admin', 'ad', 'min', '1234567890', 'admin@gmail.com', '$2a$06$gifP.ONgKX9iYCG2KmXFiurbtevbtfaeIKWlmfVaNJ/yDfvnT0CI.', true);
INSERT INTO public.user_details (username, fname, lname, phno, emailid, password, "isClient") VALUES ('dev', 'Prabhat', 'Singh', '7894561230', 'dev.704700@gmail.com', '$2a$06$LUqds14Y28cCXr7jGfSkjezzYBcXLp5cBslPO/4so.NPeGtn9HaNq', false);
INSERT INTO public.user_details (username, fname, lname, phno, emailid, password, "isClient") VALUES ('ab', 'a', 'b', '1234567890', 'ab@gmail.com', '$2a$06$UnxPWvMJ6oLS/uDhvTx2xeRfoFCcT1T3UKbumWq/S6vxoWdKs4b4y', true);


--
-- TOC entry 2926 (class 2606 OID 17612)
-- Name: category category_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.category
    ADD CONSTRAINT category_pkey PRIMARY KEY (gameid, cat_name);


--
-- TOC entry 2922 (class 2606 OID 17586)
-- Name: game game_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game
    ADD CONSTRAINT game_pkey PRIMARY KEY (game_name, date_of_release);


--
-- TOC entry 2924 (class 2606 OID 17599)
-- Name: identty identty_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.identty
    ADD CONSTRAINT identty_pkey PRIMARY KEY (gameid);


--
-- TOC entry 2930 (class 2606 OID 17643)
-- Name: ratereview ratereview_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ratereview
    ADD CONSTRAINT ratereview_pkey PRIMARY KEY (gameid, username);


--
-- TOC entry 2928 (class 2606 OID 17625)
-- Name: transactions transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_pkey PRIMARY KEY (gameid, username);


--
-- TOC entry 2920 (class 2606 OID 17578)
-- Name: user_details user_details_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_details
    ADD CONSTRAINT user_details_pkey PRIMARY KEY (username);


--
-- TOC entry 2940 (class 2620 OID 17667)
-- Name: game futurerelease; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE CONSTRAINT TRIGGER futurerelease AFTER INSERT OR UPDATE ON public.game NOT DEFERRABLE INITIALLY IMMEDIATE FOR EACH ROW EXECUTE FUNCTION public."noReleases_in_future"();


--
-- TOC entry 2942 (class 2620 OID 17671)
-- Name: transactions futuresales; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE CONSTRAINT TRIGGER futuresales AFTER INSERT OR UPDATE ON public.transactions NOT DEFERRABLE INITIALLY IMMEDIATE FOR EACH ROW EXECUTE FUNCTION public."noSales_in_future"();


--
-- TOC entry 2941 (class 2620 OID 17665)
-- Name: game insertidentty; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE CONSTRAINT TRIGGER insertidentty AFTER INSERT ON public.game NOT DEFERRABLE INITIALLY IMMEDIATE FOR EACH ROW EXECUTE FUNCTION public."autoInsert_identty"();


--
-- TOC entry 2938 (class 2620 OID 17669)
-- Name: user_details passwordlimit; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE CONSTRAINT TRIGGER passwordlimit AFTER INSERT OR UPDATE ON public.user_details NOT DEFERRABLE INITIALLY IMMEDIATE FOR EACH ROW EXECUTE FUNCTION public.password_limit();


--
-- TOC entry 2939 (class 2620 OID 17678)
-- Name: user_details phnocheck; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE CONSTRAINT TRIGGER phnocheck AFTER INSERT OR UPDATE ON public.user_details NOT DEFERRABLE INITIALLY IMMEDIATE FOR EACH ROW EXECUTE FUNCTION public.phno_limit();


--
-- TOC entry 2943 (class 2620 OID 17673)
-- Name: transactions sellrelease; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE CONSTRAINT TRIGGER sellrelease AFTER INSERT OR UPDATE ON public.transactions NOT DEFERRABLE INITIALLY IMMEDIATE FOR EACH ROW EXECUTE FUNCTION public.sell_after_release();


--
-- TOC entry 2933 (class 2606 OID 17613)
-- Name: category category_gameid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.category
    ADD CONSTRAINT category_gameid_fkey FOREIGN KEY (gameid) REFERENCES public.identty(gameid);


--
-- TOC entry 2931 (class 2606 OID 17587)
-- Name: game game_username_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game
    ADD CONSTRAINT game_username_fkey FOREIGN KEY (username) REFERENCES public.user_details(username) ON DELETE SET NULL;


--
-- TOC entry 2932 (class 2606 OID 17600)
-- Name: identty identty_gamename_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.identty
    ADD CONSTRAINT identty_gamename_fkey FOREIGN KEY (date_of_release, game_name) REFERENCES public.game(date_of_release, game_name);


--
-- TOC entry 2936 (class 2606 OID 17644)
-- Name: ratereview ratereview_gameid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ratereview
    ADD CONSTRAINT ratereview_gameid_fkey FOREIGN KEY (gameid) REFERENCES public.identty(gameid);


--
-- TOC entry 2937 (class 2606 OID 17649)
-- Name: ratereview ratereview_username_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ratereview
    ADD CONSTRAINT ratereview_username_fkey FOREIGN KEY (username) REFERENCES public.user_details(username);


--
-- TOC entry 2934 (class 2606 OID 17626)
-- Name: transactions transaction_gameid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transaction_gameid_fkey FOREIGN KEY (gameid) REFERENCES public.identty(gameid) ON DELETE SET NULL;


--
-- TOC entry 2935 (class 2606 OID 17631)
-- Name: transactions transaction_username_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transaction_username_fkey FOREIGN KEY (username) REFERENCES public.user_details(username);


-- Completed on 2020-12-17 20:29:46

--
-- PostgreSQL database dump complete
--

