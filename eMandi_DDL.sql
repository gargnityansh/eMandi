--
-- PostgreSQL database dump
--

-- Dumped from database version 14.0
-- Dumped by pg_dump version 14.0

-- Started on 2021-10-25 15:22:06

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 213 (class 1259 OID 16436)
-- Name: Auction; Type: TABLE; Schema: public; Owner: postgres
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- TOC entry 3086 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


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
-- TOC entry 210 (class 1259 OID 16415)
-- Name: Auditor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Auditor" (
    a_username character varying NOT NULL,
    auditor_name character varying NOT NULL,
    a_email character varying,
    a_password text NOT NULL,
    "a_phoneNo" numeric(10,0) NOT NULL
);


ALTER TABLE public."Auditor" OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 16422)
-- Name: Buyer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Buyer" (
    b_username character varying NOT NULL,
    buyer_name character varying NOT NULL,
    b_kyc_flag boolean NOT NULL,
    b_upi character varying(30) NOT NULL,
    buyer_loc character varying(30) NOT NULL,
    buyer_city character varying(30) NOT NULL,
    buyer_state character varying(30) NOT NULL,
    b_password text NOT NULL,
    b_email character varying,
    "b_phoneNo" numeric(10,0) NOT NULL
);


ALTER TABLE public."Buyer" OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 16448)
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
-- TOC entry 215 (class 1259 OID 16470)
-- Name: Crop; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Crop" (
    "crop_ID" character varying NOT NULL,
    crop_type character varying,
    crop_city character varying(30) NOT NULL,
    crop_name character varying(30) NOT NULL,
    "upload_Date" date NOT NULL,
    final_bid_price numeric,
    crop_grade character varying,
    "grading_Date" date,
    min_bid_price numeric,
    "pickup_Date" date,
    "delivery_Date" date,
    buyer_loc character varying(30),
    buyer_city character varying(30),
    buyer_state character varying(30),
    farmer_loc character varying(30),
    farmer_city character varying(30),
    farmer_state character varying(30),
    f_username character varying NOT NULL,
    "auction_ID" character varying,
    a_username character varying,
    "truck_chasisNo" character varying(17)
);


ALTER TABLE public."Crop" OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 16408)
-- Name: Farmer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Farmer" (
    f_username character varying NOT NULL,
    farmer_name character varying NOT NULL,
    f_kyc_flag boolean NOT NULL,
    f_upi character varying(30) NOT NULL,
    farmer_loc character varying(30) NOT NULL,
    farmer_city character varying(30) NOT NULL,
    farmer_state character varying(30) NOT NULL,
    f_password text NOT NULL,
    f_email character varying,
    "f_phoneNo" numeric(10,0) NOT NULL
);


ALTER TABLE public."Farmer" OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 16429)
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
-- TOC entry 3196 (class 2606 OID 16442)
-- Name: Auction auction_PK; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Auction"
    ADD CONSTRAINT "auction_PK" PRIMARY KEY ("auction_ID");


--
-- TOC entry 3190 (class 2606 OID 16421)
-- Name: Auditor auditor_PK; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Auditor"
    ADD CONSTRAINT "auditor_PK" PRIMARY KEY (a_username);


--
-- TOC entry 3192 (class 2606 OID 16428)
-- Name: Buyer buyer_PK; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Buyer"
    ADD CONSTRAINT "buyer_PK" PRIMARY KEY (b_username);


--
-- TOC entry 3198 (class 2606 OID 16454)
-- Name: Complaint complaint_PK; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Complaint"
    ADD CONSTRAINT "complaint_PK" PRIMARY KEY ("complaint_ID");


--
-- TOC entry 3200 (class 2606 OID 16476)
-- Name: Crop crop_PK; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Crop"
    ADD CONSTRAINT "crop_PK" PRIMARY KEY ("crop_ID");


--
-- TOC entry 3188 (class 2606 OID 16414)
-- Name: Farmer farmer_PK; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Farmer"
    ADD CONSTRAINT "farmer_PK" PRIMARY KEY (f_username);


--
-- TOC entry 3194 (class 2606 OID 16435)
-- Name: Truck truck_PK; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Truck"
    ADD CONSTRAINT "truck_PK" PRIMARY KEY ("truck_chasisNo");


--
-- TOC entry 3201 (class 2606 OID 16443)
-- Name: Auction auction_buyer_FK; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Auction"
    ADD CONSTRAINT "auction_buyer_FK" FOREIGN KEY (b_username) REFERENCES public."Buyer"(b_username) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3205 (class 2606 OID 16477)
-- Name: Crop auction_crop_FK; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Crop"
    ADD CONSTRAINT "auction_crop_FK" FOREIGN KEY ("auction_ID") REFERENCES public."Auction"("auction_ID") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3206 (class 2606 OID 16482)
-- Name: Crop auditor_crop_FK; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Crop"
    ADD CONSTRAINT "auditor_crop_FK" FOREIGN KEY (a_username) REFERENCES public."Auditor"(a_username) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3204 (class 2606 OID 16465)
-- Name: Complaint complaint_auditor_FK; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Complaint"
    ADD CONSTRAINT "complaint_auditor_FK" FOREIGN KEY (a_username) REFERENCES public."Auditor"(a_username);


--
-- TOC entry 3202 (class 2606 OID 16455)
-- Name: Complaint complaint_buyer_Fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Complaint"
    ADD CONSTRAINT "complaint_buyer_Fk" FOREIGN KEY (b_username) REFERENCES public."Buyer"(b_username);


--
-- TOC entry 3203 (class 2606 OID 16460)
-- Name: Complaint complaint_farmer_Fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Complaint"
    ADD CONSTRAINT "complaint_farmer_Fk" FOREIGN KEY (f_username) REFERENCES public."Farmer"(f_username);


--
-- TOC entry 3208 (class 2606 OID 16492)
-- Name: Crop farmer_crop_FK; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Crop"
    ADD CONSTRAINT "farmer_crop_FK" FOREIGN KEY (f_username) REFERENCES public."Farmer"(f_username) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3207 (class 2606 OID 16487)
-- Name: Crop truck_crop_FK; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Crop"
    ADD CONSTRAINT "truck_crop_FK" FOREIGN KEY ("truck_chasisNo") REFERENCES public."Truck"("truck_chasisNo") ON UPDATE CASCADE ON DELETE CASCADE;


-- Completed on 2021-10-25 15:22:07

--
-- PostgreSQL database dump complete
--

