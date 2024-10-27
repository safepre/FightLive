--
-- PostgreSQL database dump
--

-- Dumped from database version 13.16 (Debian 13.16-1.pgdg120+1)
-- Dumped by pg_dump version 13.16 (Debian 13.16-1.pgdg120+1)

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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: bobasafe
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO bobasafe;

--
-- Name: fighters; Type: TABLE; Schema: public; Owner: bobasafe
--

CREATE TABLE public.fighters (
    id integer NOT NULL,
    date_created timestamp with time zone DEFAULT now(),
    full_name character varying NOT NULL
);


ALTER TABLE public.fighters OWNER TO bobasafe;

--
-- Name: fighters_id_seq; Type: SEQUENCE; Schema: public; Owner: bobasafe
--

CREATE SEQUENCE public.fighters_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fighters_id_seq OWNER TO bobasafe;

--
-- Name: fighters_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bobasafe
--

ALTER SEQUENCE public.fighters_id_seq OWNED BY public.fighters.id;


--
-- Name: fights; Type: TABLE; Schema: public; Owner: bobasafe
--

CREATE TABLE public.fights (
    id integer NOT NULL,
    date_created timestamp with time zone DEFAULT now(),
    fighter_id integer NOT NULL,
    opponent_id integer NOT NULL,
    scorecard_id integer NOT NULL
);


ALTER TABLE public.fights OWNER TO bobasafe;

--
-- Name: fights_id_seq; Type: SEQUENCE; Schema: public; Owner: bobasafe
--

CREATE SEQUENCE public.fights_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fights_id_seq OWNER TO bobasafe;

--
-- Name: fights_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bobasafe
--

ALTER SEQUENCE public.fights_id_seq OWNED BY public.fights.id;


--
-- Name: scorecards; Type: TABLE; Schema: public; Owner: bobasafe
--

CREATE TABLE public.scorecards (
    id integer NOT NULL,
    date_created timestamp with time zone DEFAULT now(),
    link character varying NOT NULL
);


ALTER TABLE public.scorecards OWNER TO bobasafe;

--
-- Name: scorecards_id_seq; Type: SEQUENCE; Schema: public; Owner: bobasafe
--

CREATE SEQUENCE public.scorecards_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.scorecards_id_seq OWNER TO bobasafe;

--
-- Name: scorecards_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bobasafe
--

ALTER SEQUENCE public.scorecards_id_seq OWNED BY public.scorecards.id;


--
-- Name: fighters id; Type: DEFAULT; Schema: public; Owner: bobasafe
--

ALTER TABLE ONLY public.fighters ALTER COLUMN id SET DEFAULT nextval('public.fighters_id_seq'::regclass);


--
-- Name: fights id; Type: DEFAULT; Schema: public; Owner: bobasafe
--

ALTER TABLE ONLY public.fights ALTER COLUMN id SET DEFAULT nextval('public.fights_id_seq'::regclass);


--
-- Name: scorecards id; Type: DEFAULT; Schema: public; Owner: bobasafe
--

ALTER TABLE ONLY public.scorecards ALTER COLUMN id SET DEFAULT nextval('public.scorecards_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: bobasafe
--

COPY public.alembic_version (version_num) FROM stdin;
c2132a65231b
\.


--
-- Data for Name: fighters; Type: TABLE DATA; Schema: public; Owner: bobasafe
--

COPY public.fighters (id, date_created, full_name) FROM stdin;
1	2024-10-04 20:31:39.52257+00	Sean O’Malley
2	2024-10-04 20:31:39.52257+00	Merab Dvalishvili
3	2024-10-04 20:31:39.719731+00	Renato Moicano
4	2024-10-04 20:31:39.719731+00	Benoît Saint Denis
5	2024-10-05 00:26:05.168008+00	Henry Cejudo
6	2024-10-05 23:52:18.85947+00	Carla Esparza
7	2024-10-05 23:52:18.85947+00	Tecia Pennington
8	2024-10-06 01:08:27.996585+00	Austin Hubbard
9	2024-10-06 01:08:27.996585+00	Alexander Hernandez
10	2024-10-06 01:43:36.793985+00	Marina Rodriguez
11	2024-10-06 01:43:36.793985+00	Iasmin Lucindo
12	2024-10-06 02:13:39.447793+00	Joaquin Buckley
13	2024-10-06 02:13:39.447793+00	Stephen Thompson
14	2024-10-06 03:13:43.406215+00	Roman Dolidze
15	2024-10-06 03:13:43.406215+00	Kevin Holland
16	2024-10-06 03:43:45.458979+00	José Aldo
17	2024-10-06 03:43:45.458979+00	Mario Bautista
18	2024-10-06 05:28:50.889396+00	Alex Pereira
19	2024-10-06 05:28:50.889396+00	Khalil Rountree Jr.
20	2024-10-06 20:12:22.014771+00	Kayla Harrison
21	2024-10-06 20:12:22.014771+00	Ketlen Vieira
22	2024-10-06 20:20:26.087877+00	Julianna Peña
23	2024-10-06 20:20:26.087877+00	Raquel Pennington
24	2024-10-12 17:55:20.72998+00	Javid Basharat
25	2024-10-12 17:55:20.72998+00	Victor Henry
26	2024-10-12 20:31:07.425927+00	Clayton Carpenter
27	2024-10-12 20:31:07.425927+00	Lucas Rocha
28	2024-10-12 21:01:09.547476+00	Dan Argueta
29	2024-10-12 21:01:09.547476+00	Cody Haddon
30	2024-10-12 21:31:11.538272+00	Julia Polastri
31	2024-10-12 21:31:11.538272+00	Cory McKenna
32	2024-10-12 21:46:12.530396+00	Junior Tafa
33	2024-10-12 21:46:12.530396+00	Sean Sharaf
34	2024-10-12 22:16:14.079724+00	Themba Gorimbo
35	2024-10-12 22:16:14.079724+00	Niko Price
36	2024-10-12 23:46:19.426711+00	Daniel Rodriguez
37	2024-10-12 23:46:19.426711+00	Alex Morono
38	2024-10-13 00:16:21.592931+00	Grant Dawson
39	2024-10-13 00:16:21.592931+00	Rafa Garcia
40	2024-10-13 00:46:23.664371+00	Chidi Njokuani
41	2024-10-13 00:46:23.664371+00	Jared Gooden
42	2024-10-13 01:16:25.661659+00	Brad Tavares
43	2024-10-13 01:16:25.661659+00	JunYong Park
44	2024-10-13 02:01:28.747604+00	Brandon Royval
45	2024-10-13 02:01:28.747604+00	Tatsuro Taira
46	2024-10-19 20:59:20.685903+00	Austen Lane
47	2024-10-19 20:59:20.685903+00	Robelis Despaigne
48	2024-10-19 21:14:22.292216+00	Melissa Martinez
49	2024-10-19 21:14:22.292216+00	Alice Ardelean
50	2024-10-19 21:47:25.388258+00	Jessica Penne
51	2024-10-19 21:47:25.388258+00	Elise Reed
52	2024-10-19 22:17:27.316774+00	Joselyne Edwards
53	2024-10-19 22:17:27.316774+00	Tamires Vidal
54	2024-10-19 22:47:29.523663+00	Brad Katona
55	2024-10-19 22:47:29.523663+00	Jean Matsumoto
56	2024-10-19 23:05:31.087688+00	Matheus Nicolau
57	2024-10-19 23:05:31.087688+00	Asu Almabayev
58	2024-10-19 23:50:33.199454+00	Darren Elkins
59	2024-10-19 23:50:33.199454+00	Daniel Pineda
60	2024-10-20 00:20:35.076611+00	Jake Hadley
61	2024-10-20 00:20:35.076611+00	Cameron Smotherman
62	2024-10-20 00:50:36.844711+00	Charles Johnson
63	2024-10-20 00:50:36.844711+00	Sumudaerji
64	2024-10-20 02:11:46.973326+00	Anthony Hernandez
65	2024-10-20 02:11:46.973326+00	Michel Pereira
66	2024-10-21 01:15:05.515+00	Rob Font
67	2024-10-21 01:15:05.515+00	Kyler Phillips
\.


--
-- Data for Name: fights; Type: TABLE DATA; Schema: public; Owner: bobasafe
--

COPY public.fights (id, date_created, fighter_id, opponent_id, scorecard_id) FROM stdin;
1	2024-10-04 20:31:39.52257+00	1	2	1
2	2024-10-04 20:31:39.719731+00	3	4	2
3	2024-10-05 00:26:05.168008+00	2	5	3
4	2024-10-05 23:52:18.85947+00	6	7	4
5	2024-10-06 01:08:27.996585+00	8	9	5
6	2024-10-06 01:43:36.793985+00	10	11	6
7	2024-10-06 02:13:39.447793+00	12	13	7
8	2024-10-06 03:13:43.406215+00	14	15	8
9	2024-10-06 03:43:45.458979+00	16	17	9
10	2024-10-06 05:28:50.889396+00	18	19	10
11	2024-10-06 20:12:22.014771+00	20	21	11
12	2024-10-06 20:20:26.087877+00	22	23	12
13	2024-10-12 17:55:20.72998+00	24	25	13
14	2024-10-12 20:31:07.425927+00	26	27	14
15	2024-10-12 21:01:09.547476+00	28	29	15
16	2024-10-12 21:31:11.538272+00	30	31	16
17	2024-10-12 21:46:12.530396+00	32	33	17
18	2024-10-12 22:16:14.079724+00	34	35	18
19	2024-10-12 23:46:19.426711+00	36	37	19
20	2024-10-13 00:16:21.592931+00	38	39	20
21	2024-10-13 00:46:23.664371+00	40	41	21
22	2024-10-13 01:16:25.661659+00	42	43	22
23	2024-10-13 02:01:28.747604+00	44	45	23
24	2024-10-19 20:59:20.685903+00	46	47	24
25	2024-10-19 21:14:22.292216+00	48	49	25
26	2024-10-19 21:47:25.388258+00	50	51	26
27	2024-10-19 22:17:27.316774+00	52	53	27
28	2024-10-19 22:47:29.523663+00	54	55	28
29	2024-10-19 23:05:31.087688+00	56	57	29
30	2024-10-19 23:50:33.199454+00	58	59	30
31	2024-10-20 00:20:35.076611+00	60	61	31
32	2024-10-20 00:50:36.844711+00	62	63	32
33	2024-10-20 02:11:46.973326+00	64	65	33
34	2024-10-21 01:15:05.515+00	66	67	34
35	2024-10-21 01:47:51.65252+00	64	65	35
36	2024-10-21 02:09:30.054013+00	64	65	36
\.


--
-- Data for Name: scorecards; Type: TABLE DATA; Schema: public; Owner: bobasafe
--

COPY public.scorecards (id, date_created, link) FROM stdin;
1	2024-10-04 20:31:39.52257+00	https://pbs.twimg.com/media/GY3TBjYXEAACMcq.jpg
2	2024-10-04 20:31:39.719731+00	https://pbs.twimg.com/media/GYycUcOXQA0De5Y.jpg
3	2024-10-05 00:26:05.168008+00	https://pbs.twimg.com/media/GZFfoAEWgAAgo0O.jpg
4	2024-10-05 23:52:18.85947+00	https://pbs.twimg.com/media/GZKeh5IaQAARNWo.jpg
5	2024-10-06 01:08:27.996585+00	https://pbs.twimg.com/media/GZKzpJba0AAnD8R.jpg
6	2024-10-06 01:43:36.793985+00	https://pbs.twimg.com/media/GZK6p-caEAAyZx1.jpg
7	2024-10-06 02:13:39.447793+00	https://pbs.twimg.com/media/GZLA5bFbIAAGfP5.jpg
8	2024-10-06 03:13:43.406215+00	https://pbs.twimg.com/media/GZLPDADbMAAyJmj.jpg
9	2024-10-06 03:43:45.458979+00	https://pbs.twimg.com/media/GZLW2uoboAAoDBy.jpg
10	2024-10-06 05:28:50.889396+00	https://pbs.twimg.com/media/GZLt21ab0AATtTG.jpg
11	2024-10-06 20:12:22.014771+00	https://pbs.twimg.com/media/GZLKYWkaoAAIUQU.jpg
12	2024-10-06 20:20:26.087877+00	https://pbs.twimg.com/media/GZLmeF0aUAAm5I9.jpg
13	2024-10-12 17:55:20.72998+00	https://pbs.twimg.com/media/GZOisM5W0AAI66M.jpg
14	2024-10-12 20:31:07.425927+00	https://pbs.twimg.com/media/GZt25CYaQAAn1cR.jpg
15	2024-10-12 21:01:09.547476+00	https://pbs.twimg.com/media/GZt-WyHaAAAWXpW.jpg
16	2024-10-12 21:31:11.538272+00	https://pbs.twimg.com/media/GZuEpCyaAAMc8uD.jpg
17	2024-10-12 21:46:12.530396+00	https://pbs.twimg.com/media/GZuJALNaAAIZg9Y.jpg
18	2024-10-12 22:16:14.079724+00	https://pbs.twimg.com/media/GZuP7rXaAAAQvYH.jpg
19	2024-10-12 23:46:19.426711+00	https://pbs.twimg.com/media/GZujTboaAAIN1wF.jpg
20	2024-10-13 00:16:21.592931+00	https://pbs.twimg.com/media/GZuoZFxbcAAXSHh.jpg
21	2024-10-13 00:46:23.664371+00	https://pbs.twimg.com/media/GZuvz1saAAITQat.jpg
22	2024-10-13 01:16:25.661659+00	https://pbs.twimg.com/media/GZu3xL6aAAY1eGU.jpg
23	2024-10-13 02:01:28.747604+00	https://pbs.twimg.com/media/GZvC1tOaAAAq1MQ.jpg
24	2024-10-19 20:59:20.685903+00	https://pbs.twimg.com/media/GaR-f_UW0AAzI31.jpg
25	2024-10-19 21:14:22.292216+00	https://pbs.twimg.com/media/GaSET73W8AA-NpR.jpg
26	2024-10-19 21:47:25.388258+00	https://pbs.twimg.com/media/GaSMEDfWQAAAgjZ.jpg
27	2024-10-19 22:17:27.316774+00	https://pbs.twimg.com/media/GaSQxgKXcAAj2JF.jpg
28	2024-10-19 22:47:29.523663+00	https://pbs.twimg.com/media/GaSX6qiX0AAvTjx.jpg
29	2024-10-19 23:05:31.087688+00	https://pbs.twimg.com/media/GaSdSwsXwAA2HBX.jpg
30	2024-10-19 23:50:33.199454+00	https://pbs.twimg.com/media/GaSmPDdXIAAiEXn.jpg
31	2024-10-20 00:20:35.076611+00	https://pbs.twimg.com/media/GaSuuVrXsAEB09r.jpg
32	2024-10-20 00:50:36.844711+00	https://pbs.twimg.com/media/GaS2TH0WIAACk5X.jpg
33	2024-10-20 02:11:46.973326+00	https://pbs.twimg.com/media/GaTHyHfWAAACzU5.jpg
34	2024-10-21 01:15:05.515+00	https://pbs.twimg.com/media/GaTOYL6WUAIIjrY.jpg
35	2024-10-21 01:47:51.65252+00	https://pbs.twimg.com/media/GaYGuTZXAAATLQ3.jpg
36	2024-10-21 02:09:30.054013+00	https://pbs.twimg.com/media/GaYPRN-WYAAeURa.jpg
\.


--
-- Name: fighters_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bobasafe
--

SELECT pg_catalog.setval('public.fighters_id_seq', 67, true);


--
-- Name: fights_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bobasafe
--

SELECT pg_catalog.setval('public.fights_id_seq', 36, true);


--
-- Name: scorecards_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bobasafe
--

SELECT pg_catalog.setval('public.scorecards_id_seq', 36, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: bobasafe
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: fighters fighters_full_name_key; Type: CONSTRAINT; Schema: public; Owner: bobasafe
--

ALTER TABLE ONLY public.fighters
    ADD CONSTRAINT fighters_full_name_key UNIQUE (full_name);


--
-- Name: fighters fighters_pkey; Type: CONSTRAINT; Schema: public; Owner: bobasafe
--

ALTER TABLE ONLY public.fighters
    ADD CONSTRAINT fighters_pkey PRIMARY KEY (id);


--
-- Name: fights fights_pkey; Type: CONSTRAINT; Schema: public; Owner: bobasafe
--

ALTER TABLE ONLY public.fights
    ADD CONSTRAINT fights_pkey PRIMARY KEY (id);


--
-- Name: scorecards scorecards_pkey; Type: CONSTRAINT; Schema: public; Owner: bobasafe
--

ALTER TABLE ONLY public.scorecards
    ADD CONSTRAINT scorecards_pkey PRIMARY KEY (id);


--
-- Name: fights fights_fighter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bobasafe
--

ALTER TABLE ONLY public.fights
    ADD CONSTRAINT fights_fighter_id_fkey FOREIGN KEY (fighter_id) REFERENCES public.fighters(id);


--
-- Name: fights fights_opponent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bobasafe
--

ALTER TABLE ONLY public.fights
    ADD CONSTRAINT fights_opponent_id_fkey FOREIGN KEY (opponent_id) REFERENCES public.fighters(id);


--
-- Name: fights fights_scorecard_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bobasafe
--

ALTER TABLE ONLY public.fights
    ADD CONSTRAINT fights_scorecard_id_fkey FOREIGN KEY (scorecard_id) REFERENCES public.scorecards(id);


--
-- PostgreSQL database dump complete
--

