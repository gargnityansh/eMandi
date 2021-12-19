--
-- PostgreSQL database dump
--

-- Dumped from database version 13.4
-- Dumped by pg_dump version 13.4

-- Started on 2021-12-19 14:50:49

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
-- TOC entry 2 (class 3079 OID 25369)
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- TOC entry 3074 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 201 (class 1259 OID 25406)
-- Name: Auction; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Auction" (
    "auction_ID" character varying NOT NULL,
    "a_startDate" date,
    "a_endDate" date,
    bid_date date NOT NULL,
    bid_time time without time zone NOT NULL,
    "bidAmount" numeric NOT NULL,
    b_username character varying NOT NULL
);


ALTER TABLE public."Auction" OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 25412)
-- Name: Auditor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Auditor" (
    a_username character varying NOT NULL,
    auditor_name character varying NOT NULL,
    a_email character varying,
    a_password text NOT NULL,
    a_phno character varying NOT NULL
);


ALTER TABLE public."Auditor" OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 25418)
-- Name: Buyer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Buyer" (
    b_username character varying NOT NULL,
    buyer_name character varying NOT NULL,
    buyer_loc character varying(30) NOT NULL,
    buyer_city character varying(30) NOT NULL,
    buyer_state character varying(30) NOT NULL,
    b_password text NOT NULL,
    b_email character varying NOT NULL,
    b_phone character varying NOT NULL
);


ALTER TABLE public."Buyer" OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 25424)
-- Name: Complaint; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Complaint" (
    "complaint_ID" character varying NOT NULL,
    "curr_Grade" character varying NOT NULL,
    comp_date date,
    comp_time time without time zone,
    "upgraded_Grade" character varying,
    a_username character varying NOT NULL,
    f_username character varying NOT NULL,
    b_username character varying
);


ALTER TABLE public."Complaint" OWNER TO postgres;

--
-- TOC entry 205 (class 1259 OID 25430)
-- Name: Crop; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Crop" (
    "crop_ID" character varying NOT NULL,
    crop_type character varying,
    crop_region character varying(30) NOT NULL,
    crop_name character varying(30) NOT NULL,
    "upload_Date" date NOT NULL,
    final_bid_price numeric,
    crop_grade character varying,
    "grading_Date" date,
    min_bid_price numeric,
    "pickup_Date" date,
    "delivery_Date" date,
    f_username character varying NOT NULL,
    "auction_ID" character varying,
    a_username character varying,
    "truck_chasisNo" character varying(17),
    b_username character varying,
    crop_img text,
    crop_weight_kg numeric NOT NULL
);


ALTER TABLE public."Crop" OWNER TO postgres;

--
-- TOC entry 206 (class 1259 OID 25436)
-- Name: Farmer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Farmer" (
    f_username character varying NOT NULL,
    farmer_name character varying NOT NULL,
    farmer_loc character varying(30) NOT NULL,
    farmer_city character varying(30) NOT NULL,
    farmer_state character varying(30) NOT NULL,
    f_password text NOT NULL,
    f_email character varying NOT NULL,
    f_phone character varying NOT NULL
);


ALTER TABLE public."Farmer" OWNER TO postgres;

--
-- TOC entry 207 (class 1259 OID 25442)
-- Name: Truck; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Truck" (
    "truck_chasisNo" character varying(17) NOT NULL,
    truck_origin_loc character varying NOT NULL,
    truck_origin_city character varying NOT NULL,
    truck_origin_state character varying NOT NULL,
    truck_nameplate character varying(10) NOT NULL
);


ALTER TABLE public."Truck" OWNER TO postgres;

--
-- TOC entry 2917 (class 2606 OID 25449)
-- Name: Auction auction_PK; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Auction"
    ADD CONSTRAINT "auction_PK" PRIMARY KEY ("auction_ID");


--
-- TOC entry 2919 (class 2606 OID 25451)
-- Name: Auditor auditor_PK; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Auditor"
    ADD CONSTRAINT "auditor_PK" PRIMARY KEY (a_username);


--
-- TOC entry 2921 (class 2606 OID 25453)
-- Name: Buyer buyer_PK; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Buyer"
    ADD CONSTRAINT "buyer_PK" PRIMARY KEY (b_username);


--
-- TOC entry 2923 (class 2606 OID 25455)
-- Name: Complaint complaint_PK; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Complaint"
    ADD CONSTRAINT "complaint_PK" PRIMARY KEY ("complaint_ID");


--
-- TOC entry 2925 (class 2606 OID 25457)
-- Name: Crop crop_PK; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Crop"
    ADD CONSTRAINT "crop_PK" PRIMARY KEY ("crop_ID");


--
-- TOC entry 2927 (class 2606 OID 25459)
-- Name: Farmer farmer_PK; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Farmer"
    ADD CONSTRAINT "farmer_PK" PRIMARY KEY (f_username);


--
-- TOC entry 2929 (class 2606 OID 25461)
-- Name: Truck truck_PK; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Truck"
    ADD CONSTRAINT "truck_PK" PRIMARY KEY ("truck_chasisNo");


--
-- TOC entry 2930 (class 2606 OID 25462)
-- Name: Auction auction_buyer_FK; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Auction"
    ADD CONSTRAINT "auction_buyer_FK" FOREIGN KEY (b_username) REFERENCES public."Buyer"(b_username) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2934 (class 2606 OID 25467)
-- Name: Crop auction_crop_FK; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Crop"
    ADD CONSTRAINT "auction_crop_FK" FOREIGN KEY ("auction_ID") REFERENCES public."Auction"("auction_ID") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2935 (class 2606 OID 25472)
-- Name: Crop auditor_crop_FK; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Crop"
    ADD CONSTRAINT "auditor_crop_FK" FOREIGN KEY (a_username) REFERENCES public."Auditor"(a_username) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2938 (class 2606 OID 25502)
-- Name: Crop buyer_crop_FK; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Crop"
    ADD CONSTRAINT "buyer_crop_FK" FOREIGN KEY (b_username) REFERENCES public."Buyer"(b_username) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- TOC entry 2931 (class 2606 OID 25477)
-- Name: Complaint complaint_auditor_FK; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Complaint"
    ADD CONSTRAINT "complaint_auditor_FK" FOREIGN KEY (a_username) REFERENCES public."Auditor"(a_username);


--
-- TOC entry 2932 (class 2606 OID 25482)
-- Name: Complaint complaint_buyer_Fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Complaint"
    ADD CONSTRAINT "complaint_buyer_Fk" FOREIGN KEY (b_username) REFERENCES public."Buyer"(b_username);


--
-- TOC entry 2933 (class 2606 OID 25487)
-- Name: Complaint complaint_farmer_Fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Complaint"
    ADD CONSTRAINT "complaint_farmer_Fk" FOREIGN KEY (f_username) REFERENCES public."Farmer"(f_username);


--
-- TOC entry 2936 (class 2606 OID 25492)
-- Name: Crop farmer_crop_FK; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Crop"
    ADD CONSTRAINT "farmer_crop_FK" FOREIGN KEY (f_username) REFERENCES public."Farmer"(f_username) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2937 (class 2606 OID 25497)
-- Name: Crop truck_crop_FK; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Crop"
    ADD CONSTRAINT "truck_crop_FK" FOREIGN KEY ("truck_chasisNo") REFERENCES public."Truck"("truck_chasisNo") ON UPDATE CASCADE ON DELETE CASCADE;


-- Completed on 2021-12-19 14:50:50

--
-- PostgreSQL database dump complete
--

