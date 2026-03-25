--
-- PostgreSQL database dump
--

\restrict 1qvjUFRnOoAmLRlx1l4qRrPbfkdwyr89AfN5zgj5DU6uSk5odANbqVrWuL7zRRQ

-- Dumped from database version 18.2
-- Dumped by pg_dump version 18.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: assessments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.assessments (
    id integer NOT NULL,
    subject_id integer,
    week_number integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.assessments OWNER TO postgres;

--
-- Name: assessments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.assessments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.assessments_id_seq OWNER TO postgres;

--
-- Name: assessments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.assessments_id_seq OWNED BY public.assessments.id;


--
-- Name: mcq_cache; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mcq_cache (
    cache_key text NOT NULL,
    ai_data jsonb,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.mcq_cache OWNER TO postgres;

--
-- Name: options; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.options (
    id integer NOT NULL,
    question_id integer,
    option_text text,
    is_correct boolean DEFAULT false,
    media_type character varying(10),
    media_content text
);


ALTER TABLE public.options OWNER TO postgres;

--
-- Name: options_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.options_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.options_id_seq OWNER TO postgres;

--
-- Name: options_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.options_id_seq OWNED BY public.options.id;


--
-- Name: questions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.questions (
    id integer NOT NULL,
    assessment_id integer,
    heading text NOT NULL,
    media_type character varying(10),
    media_content text,
    q_type character varying(20) DEFAULT 'mcq'::character varying,
    correct_answer text
);


ALTER TABLE public.questions OWNER TO postgres;

--
-- Name: questions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.questions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.questions_id_seq OWNER TO postgres;

--
-- Name: questions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.questions_id_seq OWNED BY public.questions.id;


--
-- Name: subjects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subjects (
    id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.subjects OWNER TO postgres;

--
-- Name: subjects_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.subjects_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.subjects_id_seq OWNER TO postgres;

--
-- Name: subjects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.subjects_id_seq OWNED BY public.subjects.id;


--
-- Name: video_cache; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.video_cache (
    video_id text NOT NULL,
    ai_data jsonb,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.video_cache OWNER TO postgres;

--
-- Name: weeks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.weeks (
    id integer NOT NULL,
    subject_id integer,
    week_number integer NOT NULL,
    youtube_urls text[]
);


ALTER TABLE public.weeks OWNER TO postgres;

--
-- Name: weeks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.weeks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.weeks_id_seq OWNER TO postgres;

--
-- Name: weeks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.weeks_id_seq OWNED BY public.weeks.id;


--
-- Name: assessments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assessments ALTER COLUMN id SET DEFAULT nextval('public.assessments_id_seq'::regclass);


--
-- Name: options id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.options ALTER COLUMN id SET DEFAULT nextval('public.options_id_seq'::regclass);


--
-- Name: questions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questions ALTER COLUMN id SET DEFAULT nextval('public.questions_id_seq'::regclass);


--
-- Name: subjects id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subjects ALTER COLUMN id SET DEFAULT nextval('public.subjects_id_seq'::regclass);


--
-- Name: weeks id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.weeks ALTER COLUMN id SET DEFAULT nextval('public.weeks_id_seq'::regclass);


--
-- Data for Name: assessments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.assessments (id, subject_id, week_number, name) FROM stdin;
1	1	1	Activity 1
2	1	1	Activity 2
3	1	1	Activity 3
4	1	1	Activity 4
5	1	1	Activity 5
6	1	1	Activity 6
7	1	1	Graded Assignment
8	1	1	Practice Assignment
9	1	2	Graded Assignment
10	1	2	Practice Assignment
11	6	1	Activity 1
12	6	1	Activity 2
13	6	1	Activity 3
14	6	1	Activity 4
15	6	1	Activity 5
16	6	1	Activity 6
17	6	1	Activity 7
18	6	1	Graded Assignment
19	6	1	Practice Assignment
20	6	2	Graded Assignment
21	6	2	Practice Assignment
22	6	3	Practice Assignment
23	7	1	Activity 1
24	7	1	Activity 2
25	7	1	Activity 3
26	7	1	Activity 4
27	7	1	Activity 5
28	7	1	Activity 6
29	7	1	Graded Assignment
30	7	1	Practice Assignment
31	7	2	Graded Assignment
32	7	2	Practice Assignment
33	8	1	Graded Assignment
34	8	1	Practice Assignment
35	8	2	Graded Assignment
36	8	2	Practice Assignment
37	7	3	Activity 1
38	7	3	Activity 2
39	7	3	Activity 3
40	7	3	Activity 4
41	7	3	Activity 5
42	7	3	Practice Assignment
43	2	1	Graded Assignment
44	7	4	Practice Assignment
45	7	4	Activity 1
46	7	4	Activity 2
47	7	4	Activity 3
48	7	4	Activity 4
49	7	4	Activity 5
50	7	3	Graded Assignment
51	7	2	Activity 1
52	7	2	Activity 2
53	7	2	Activity 3
54	7	2	Activity 4
55	7	2	Activity 5
56	7	5	Activity 1
57	7	5	Activity 2
58	7	5	Activity 3
59	7	5	Activity 4
60	7	5	Activity 5
61	7	5	Practice Assignment
62	1	4	Graded Assignment
63	1	4	Practice Assignment
64	1	4	Activity 1
65	1	3	Graded Assignment
66	1	3	Practice Assignment
67	1	3	Activity 1
68	1	2	Activity 6
69	1	2	Activity 5
70	1	2	Activity 4
71	1	2	Activity 3
72	1	2	Activity 2
73	1	2	Activity 1
74	7	5	Graded Assignment
75	7	6	Activity 1
76	7	6	Activity 2
77	7	6	Activity 3
78	7	6	Activity 4
79	7	6	Practice Assignment
80	7	6	Graded Assignment
\.


--
-- Data for Name: mcq_cache; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mcq_cache (cache_key, ai_data, updated_at) FROM stdin;
mcq_565	{"code_trace": "N/A", "math_steps": "$$\\nA=\\\\begin{bmatrix} 1 & 1 & 0 \\\\\\\\ 1 & 0 & 1 \\\\\\\\ 0 & 0 & 0 \\\\\\\\ 1 & 1 & 0 \\\\end{bmatrix}\\n$$\\n\\n- **Step 1: Compute $A^TA$.**\\n\\nFirst, find $A^T$: \\n$$\\nA^T = \\\\begin{bmatrix} 1 & 1 & 0 & 1 \\\\\\\\ 1 & 0 & 0 & 1 \\\\\\\\ 0 & 1 & 0 & 0 \\\\end{bmatrix}\\n$$\\n\\nNow, compute $A^TA$: \\n$$\\nA^TA = \\\\begin{bmatrix} 1 & 1 & 0 & 1 \\\\\\\\ 1 & 0 & 0 & 1 \\\\\\\\ 0 & 1 & 0 & 0 \\\\end{bmatrix} \\\\begin{bmatrix} 1 & 1 & 0 \\\\\\\\ 1 & 0 & 1 \\\\\\\\ 0 & 0 & 0 \\\\\\\\ 1 & 1 & 0 \\\\end{bmatrix}\\n$$\\n$$\\nA^TA = \\\\begin{bmatrix}\\n(1)(1)+(1)(1)+(0)(0)+(1)(1) & (1)(1)+(1)(0)+(0)(0)+(1)(1) & (1)(0)+(1)(1)+(0)(0)+(1)(0) \\\\\\\\\\n(1)(1)+(0)(1)+(0)(0)+(1)(1) & (1)(1)+(0)(0)+(0)(0)+(1)(1) & (1)(0)+(0)(1)+(0)(0)+(1)(0) \\\\\\\\\\n(0)(1)+(1)(1)+(0)(0)+(0)(1) & (0)(1)+(1)(0)+(0)(0)+(0)(1) & (0)(0)+(1)(1)+(0)(0)+(0)(0)\\n\\\\end{bmatrix}\\n$$\\n$$\\nA^TA = \\\\begin{bmatrix} 3 & 2 & 1 \\\\\\\\ 2 & 2 & 0 \\\\\\\\ 1 & 0 & 1 \\\\end{bmatrix}\\n$$\\n\\n- **Step 2: Find the eigenvalues of $A^TA$.**\\n\\nWe solve the characteristic equation $\\\\det(A^TA - \\\\lambda I) = 0$: \\n$$\\n\\\\det\\\\begin{bmatrix} 3-\\\\lambda & 2 & 1 \\\\\\\\ 2 & 2-\\\\lambda & 0 \\\\\\\\ 1 & 0 & 1-\\\\lambda \\\\end{bmatrix} = 0\\n$$\\nExpand the determinant along the third column for simplicity: \\n$$\\n1 \\\\cdot [2 \\\\cdot 0 - (2-\\\\lambda) \\\\cdot 1] - 0 \\\\cdot [(3-\\\\lambda) \\\\cdot 0 - 2 \\\\cdot 1] + (1-\\\\lambda) \\\\cdot [(3-\\\\lambda)(2-\\\\lambda) - 2 \\\\cdot 2] = 0\\n$$\\n$$\\n-(2-\\\\lambda) + (1-\\\\lambda)[(6 - 5\\\\lambda + \\\\lambda^2) - 4] = 0\\n$$\\n$$\\n-2 + \\\\lambda + (1-\\\\lambda)(\\\\lambda^2 - 5\\\\lambda + 2) = 0\\n$$\\n$$\\n-2 + \\\\lambda + (\\\\lambda^2 - 5\\\\lambda + 2 - \\\\lambda^3 + 5\\\\lambda^2 - 2\\\\lambda) = 0\\n$$\\n$$\\n-2 + \\\\lambda + \\\\lambda^2 - 5\\\\lambda + 2 - \\\\lambda^3 + 5\\\\lambda^2 - 2\\\\lambda = 0\\n$$\\nCombine like terms: \\n$$\\n-\\\\lambda^3 + (1+5)\\\\lambda^2 + (1-5-2)\\\\lambda + (-2+2) = 0\\n$$\\n$$\\n-\\\\lambda^3 + 6\\\\lambda^2 - 6\\\\lambda = 0\\n$$\\nFactor out $-\\\\lambda$: \\n$$\\n-\\\\lambda (\\\\lambda^2 - 6\\\\lambda + 6) = 0\\n$$\\n\\n- **Step 3: Solve for $\\\\lambda$.**\\n\\nOne eigenvalue is $\\\\lambda_1 = 0$.\\nFor the other eigenvalues, solve the quadratic equation $\\\\lambda^2 - 6\\\\lambda + 6 = 0$ using the quadratic formula $\\\\lambda = \\\\frac{-b \\\\pm \\\\sqrt{b^2 - 4ac}}{2a}$: \\n$$\\n\\\\lambda = \\\\frac{-(-6) \\\\pm \\\\sqrt{(-6)^2 - 4(1)(6)}}{2(1)}\\n$$\\n$$\\n\\\\lambda = \\\\frac{6 \\\\pm \\\\sqrt{36 - 24}}{2}\\n$$\\n$$\\n\\\\lambda = \\\\frac{6 \\\\pm \\\\sqrt{12}}{2}\\n$$\\n$$\\n\\\\lambda = \\\\frac{6 \\\\pm 2\\\\sqrt{3}}{2}\\n$$\\nThis gives two more eigenvalues: \\n$$\\n\\\\lambda_2 = 3 + \\\\sqrt{3}\\n$$\\n$$\\n\\\\lambda_3 = 3 - \\\\sqrt{3}\\n$$\\n\\n- **Step 4: Identify the non-zero eigenvalues.**\\n\\nThe non-zero eigenvalues are $3 + \\\\sqrt{3}$ and $3 - \\\\sqrt{3}$.\\n\\n- **Step 5: Calculate the non-zero singular values.**\\n\\nThe singular values are the square roots of the non-zero eigenvalues of $A^TA$: \\n$$\\n\\\\sigma_1 = \\\\sqrt{3 + \\\\sqrt{3}}\\n$$\\n$$\\n\\\\sigma_2 = \\\\sqrt{3 - \\\\sqrt{3}}\\n$$\\nThus, the non-zero singular values are $\\\\sqrt{3+\\\\sqrt{3}}, \\\\sqrt{3-\\\\sqrt{3}}$.", "step_by_step": "- **Step 1: Compute the transpose of A ($A^T$) and the product $A^TA$.**\\n  - The transpose of $A$ involves swapping rows and columns. Then, perform matrix multiplication of $A^T$ and $A$.\\n- **Step 2: Find the eigenvalues of $A^TA$.**\\n  - To do this, calculate the characteristic polynomial by solving $\\\\det(A^TA - \\\\lambda I) = 0$, where $I$ is the identity matrix and $\\\\lambda$ represents the eigenvalues. This will result in a cubic polynomial in $\\\\lambda$.\\n- **Step 3: Solve the characteristic polynomial for $\\\\lambda$.**\\n  - Factor out common terms or use algebraic methods to find the roots of the polynomial. One root is typically obvious, and the remaining roots can be found using the quadratic formula if it reduces to a quadratic equation.\\n- **Step 4: Identify the non-zero eigenvalues.**\\n  - From the calculated eigenvalues, distinguish between those that are zero and those that are not.\\n- **Step 5: Calculate the non-zero singular values.**\\n  - The singular values ($\\\\\\\\sigma$) of matrix $A$ are the :green[square roots] of the non-zero eigenvalues ($\\\\\\\\lambda$) of $A^TA$. Take the positive square root for each non-zero eigenvalue.", "core_concepts": ["Singular Value Decomposition (SVD)", "Eigenvalues and Eigenvectors", "Matrix Transpose", "Matrix Multiplication", "Characteristic Polynomial", "Quadratic Formula"], "choice_analysis": "- The :green[correct choice] is option B, which states that the non-zero singular values are $\\\\sqrt{3+\\\\sqrt{3}}, \\\\sqrt{3-\\\\sqrt{3}}$.\\n- This answer is derived by first computing the matrix product $A^TA$, then finding its eigenvalues, and finally taking the :blue[square root] of the :orange[non-zero eigenvalues].\\n- The eigenvalues of $A^TA$ were found to be $0, 3+\\\\sqrt{3}, 3-\\\\sqrt{3}$.\\n- Taking the square root of the non-zero eigenvalues, $3+\\\\sqrt{3}$ and $3-\\\\sqrt{3}$, directly yields $\\\\sqrt{3+\\\\sqrt{3}}$ and $\\\\sqrt{3-\\\\sqrt{3}}$, matching option B.", "mermaid_diagram": "graph TD\\n    A[\\"Start: Given Matrix A\\"]\\n    B[\\"Compute A transpose: A'\\"]\\n    C[\\"Calculate A'A\\"]\\n    D[\\"Find Eigenvalues of A'A\\"]\\n    E[\\"Characteristic Equation: det(A'A - lambda I) = 0\\"]\\n    F[\\"Solve for lambda (Eigenvalues)\\"]\\n    G[\\"Identify Non-Zero Eigenvalues\\"]\\n    H[\\"Take Square Root of Non-Zero Eigenvalues\\"]\\n    I[\\"Result: Non-Zero Singular Values\\"]\\n    A --> B\\n    B --> C\\n    C --> D\\n    D --> E\\n    E --> F\\n    F --> G\\n    G --> H\\n    H --> I", "practical_relevance": "- Singular Value Decomposition (SVD) is a :blue-background[fundamental matrix factorization] technique with wide-ranging applications in machine learning and data science.\\n- In :orange[dimensionality reduction], SVD is used in Principal Component Analysis (PCA) to reduce the number of features while retaining most of the variance in the data, which is crucial for efficient model training and visualization.\\n- SVD is also vital in :orange[recommender systems], where it helps decompose user-item interaction matrices to uncover latent features and predict user preferences, leading to personalized recommendations.\\n- Other applications include :orange[image compression], :orange[natural language processing] (Latent Semantic Analysis), and solving :orange[least squares problems] in regression, showcasing its versatility and importance in various computational tasks.", "common_mistake_trigger": "- A :red-background[common mistake] is to confuse the eigenvalues of $A^TA$ with the singular values of $A$. Remember that singular values ($\\\\\\\\sigma$) are the :orange[square roots] of the eigenvalues ($\\\\\\\\lambda$) of $A^TA$, i.e., $\\\\\\\\sigma = \\\\\\\\sqrt{\\\\\\\\lambda}$.\\n- Another frequent error is making :red[arithmetic mistakes] when computing the matrix product $A^TA$ or when solving for the eigenvalues of the resulting symmetric matrix, especially during the characteristic polynomial expansion and quadratic formula application.\\n- Neglecting to identify and discard the :violet[zero eigenvalues] if only non-zero singular values are requested can also lead to incorrect choices.", "wrong_options_analysis": "- Option A, '$3+\\\\sqrt{3}, 3-\\\\sqrt{3}$', represents the :red[eigenvalues] of $A^TA$, not the singular values themselves. Singular values are the square roots of the eigenvalues of $A^TA$.\\n- Option C, '$2+\\\\sqrt{2}, 2-\\\\sqrt{2}$', presents values that are :red[incorrect] both as eigenvalues and singular values for the given matrix $A$. This might result from miscalculations during the eigenvalue computation.\\n- Option D, '$\\\\sqrt{2+\\\\sqrt{2}}, \\\\sqrt{2-\\\\sqrt{2}}$', similarly provides :red[incorrect] values. This indicates a potential error in calculating the eigenvalues of $A^TA$ or misapplying the singular value definition."}	2026-03-25 18:54:34.450831
\.


--
-- Data for Name: options; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.options (id, question_id, option_text, is_correct, media_type, media_content) FROM stdin;
1	25	Java, API, Markup	f	\N	\N
2	25	JavaScript, ASP, Markup	f	\N	\N
3	25	Java, ASP, Markup	f	\N	\N
4	25	JavaScript, API, Markup	t	\N	\N
5	26	Sir Tim Berners-Lee	f	\N	\N
6	26	Roy Fielding	f	\N	\N
7	26	Mathias Biilmann	t	\N	\N
8	26	None of the above	f	\N	\N
9	62	Progressive World App	f	\N	\N
10	62	Permanent Web App	f	\N	\N
11	62	Progressive Web App	t	\N	\N
12	62	None of the above	f	\N	\N
13	63	Simple Page App	f	\N	\N
14	63	Single Page App	t	\N	\N
15	63	Single page Asset	f	\N	\N
16	63	None of the above	f	\N	\N
17	64	5000	t	\N	\N
18	64	8000	f	\N	\N
19	64	8080	f	\N	\N
20	64	3000	f	\N	\N
21	97	\N	f	code	<applet code=“appletdemo.class”> </applet>
22	97	\N	f	code	<applet code = “appletdemo” > </applet>
23	97	Both 1 and 2	t	\N	\N
24	97	None of the above	f	\N	\N
25	98	It is used to display alternative text in case the browser does not support Java.	t	\N	\N
26	98	It is used to display alternative text in case JavaScript is disabled in the browser.	f	\N	\N
27	98	It is used to display the title for the applet.	f	\N	\N
28	98	None of the above	f	\N	\N
29	99	JavaScript can be used for DOM manipulation.	t	\N	\N
30	99	Being a client side scripting language, it reduces the load on the server.	t	\N	\N
31	99	JavaScript cannot be used in the backend.	f	\N	\N
32	99	All of the above	f	\N	\N
33	109	DOM Manipulation	f	\N	\N
34	109	Asynchronous Processing	f	\N	\N
35	109	Event Loop	f	\N	\N
36	109	All of the above	t	\N	\N
37	110	It is a special program that can be run by a browser's java virtual machine.	t	\N	\N
38	110	It is a programming language.	f	\N	\N
39	110	Applets are written in java.	t	\N	\N
40	110	It can be embedded in HTML documents.	t	\N	\N
41	111	Mozilla Firefox	t	\N	\N
42	111	Google Chrome	f	\N	\N
43	111	Internet Explorer	f	\N	\N
44	111	Safari	f	\N	\N
45	112	JavaScript always requires a browser for its execution.	f	\N	\N
46	112	JavaScript cannot be invoked using command line.	f	\N	\N
47	112	JavaScript always requires a document context in order to be executed.	f	\N	\N
48	112	All of the above	t	\N	\N
49	113	5	f	\N	\N
50	113	undefined	f	\N	\N
51	113	\N	f	\N	\N
52	113	Reference Error	t	\N	\N
53	114	AJAX is an acronym for Asynchronous JavaScript and XML.	t	\N	\N
54	114	It is a technology used to send request to the server without reloading the page via JavaScript.	t	\N	\N
55	114	Only XML data can be transported using AJAX.	f	\N	\N
56	114	All of the above	f	\N	\N
57	115	undefined	t	\N	\N
58	115	\N	f	\N	\N
59	115	0	f	\N	\N
60	115	It will throw a syntax error.	f	\N	\N
61	116	It will throw a TypeError.	t	\N	\N
62	116	15	f	\N	\N
63	116	14	f	\N	\N
64	116	undefined	f	\N	\N
65	117	SyntaxError	f	\N	\N
66	117	Red	f	\N	\N
67	117	Yellow	t	\N	\N
68	117	Undefined	f	\N	\N
69	118	\N	t	code	const sum = (x, y) => {return x+y}
70	118	\N	t	code	const sum = (x, y) => x+y
71	118	\N	t	code	const sqr = x => {return x*x}
72	118	\N	t	code	const sqr = x => x*x
73	119	red	t	\N	\N
74	119	black	f	\N	\N
75	119	yellow	f	\N	\N
76	119	None of the above	f	\N	\N
77	120	black	f	\N	\N
78	120	yellow	t	\N	\N
79	120	green	f	\N	\N
80	120	red	f	\N	\N
81	121	UTF-8	f	\N	\N
82	121	UTF-16	t	\N	\N
83	121	UTF-32	f	\N	\N
84	121	ASCII	f	\N	\N
85	122	5	t	\N	\N
86	122	undefined	f	\N	\N
87	122	\N	f	\N	\N
88	122	Reference Error	f	\N	\N
89	123	==	f	\N	\N
90	123	**	f	\N	\N
91	123	===	t	\N	\N
92	123	None of the above	f	\N	\N
93	124	var	f	\N	\N
94	124	let	t	\N	\N
95	124	const	t	\N	\N
96	124	All of the above	f	\N	\N
97	125	It is a JavaScript standard.	t	\N	\N
98	125	It is a markup language.	f	\N	\N
99	125	It was designed to ensure the inter-portability of webpages across the browsers.	t	\N	\N
100	125	None of the above	f	\N	\N
101	126	const	f	\N	\N
102	126	int	t	\N	\N
103	126	while	f	\N	\N
104	126	else	f	\N	\N
105	127	\N	f	\N	\N
106	127	5	f	\N	\N
107	127	True	t	\N	\N
108	127	“IITM”	f	\N	\N
109	128	String	f	\N	\N
110	128	Number	f	\N	\N
111	128	LongInt	t	\N	\N
112	128	Boolean	f	\N	\N
113	129	def	t	\N	\N
114	129	let	f	\N	\N
115	129	const	f	\N	\N
116	129	yield	f	\N	\N
117	130	These are not objects.	t	\N	\N
118	130	Int is a primitive datatype.	f	\N	\N
119	130	Number is a primitive datatype.	t	\N	\N
120	130	undefined and null are primitive data types.	t	\N	\N
121	131	{}	t	\N	\N
122	131	\N	f	\N	\N
123	131	undefined	f	\N	\N
124	131	\N	f	\N	\N
125	65	{}	f	\N	\N
126	65	\N	f	\N	\N
127	65	undefined	t	\N	\N
128	65	\N	f	\N	\N
129	139	It will throw a syntax error.	t	\N	\N
130	139	undefined	f	\N	\N
131	139	\N	f	\N	\N
132	139	0	f	\N	\N
133	140	It will throw a TypeError.	f	\N	\N
134	140	15	t	\N	\N
135	140	14	f	\N	\N
136	140	undefined	f	\N	\N
137	141	red	f	\N	\N
138	141	green	t	\N	\N
139	141	undefined	f	\N	\N
140	141	SyntaxError	f	\N	\N
141	142	ReactJS	f	\N	\N
142	142	Flask	t	\N	\N
143	142	Bootstrap	f	\N	\N
144	142	VueJS	f	\N	\N
145	143	Flask	f	\N	\N
146	143	Django	f	\N	\N
147	143	VueJS	t	\N	\N
148	143	Express	f	\N	\N
149	144	It can manipulate the DOM.	t	\N	\N
150	144	JavaScript is a programming language.	t	\N	\N
151	144	It cannot manipulate the DOM.	f	\N	\N
152	144	None of the above	f	\N	\N
153	145	Asynchronous Java and XML	f	\N	\N
154	145	Asynchronous JavaScript and XML	t	\N	\N
155	145	Auto JavaScript and XML	f	\N	\N
156	145	None of the above	f	\N	\N
157	146	It is a study of algorithms that improve through the use of data.	f	\N	\N
158	146	It is a sub field of AI that extracts patterns out of raw data.	f	\N	\N
159	146	It allows computers to learn from experience without being explicitly programmed or human intervention.	f	\N	\N
160	146	It is used for tasks where programming/human labour fails.	f	\N	\N
161	146	All of these	t	\N	\N
162	147	Weather prediction	f	\N	\N
163	147	Face tagging	f	\N	\N
164	147	Password verification	t	\N	\N
165	147	Spam detection	f	\N	\N
166	147	Recommendation system	f	\N	\N
167	147	Social media marketing	f	\N	\N
168	148	Speech recognition	f	\N	\N
169	148	Image recognition	f	\N	\N
170	148	Object detection	f	\N	\N
171	148	Array sorting	t	\N	\N
172	149	We do not know the exact rules transforming the input to output.	t	\N	\N
173	149	There are clearly defined rules transforming the input to output.	f	\N	\N
174	149	We are unable to express the exact rules transforming the input to output.	t	\N	\N
175	150	The price of a house based on its area and distance from metro.	t	\N	\N
176	150	Whether or not a house is closer than 5 KMs to metro based on its price and area.	f	\N	\N
177	151	Continuous	t	\N	\N
178	151	Discrete	f	\N	\N
179	151	of any type	f	\N	\N
180	151	Categorical	f	\N	\N
181	152	Dimensionality Reduction	f	\N	\N
182	152	Classification	t	\N	\N
183	152	Density Estimation	f	\N	\N
184	152	Regression	t	\N	\N
185	153	Probabilistic Model	f	\N	\N
186	153	Predictive Model	t	\N	\N
187	154	$$f(X) = W^\\top X + b$$	t	\N	\N
188	154	$$f(X) = \\mathrm{Sign}(W^\\top X + b)$$	f	\N	\N
189	155	True	t	\N	\N
190	155	False	f	\N	\N
191	156	Curve fitting	t	\N	\N
192	156	Data exploration	f	\N	\N
193	156	Data cleaning	f	\N	\N
194	156	Dimensionality reduction	f	\N	\N
195	157	Probabilistic Models	f	\N	\N
196	157	Predictive Models	t	\N	\N
197	158	$$\\frac{1}{n} \\sum_{i=1}^{n} \\left( f(X^i) - Y^i \\right)^2$$	f	\N	\N
198	158	$$\\frac{1}{n} \\sum \\mathbb{1}(f(X_i) \\neq Y_i)$$	t	\N	\N
199	159	Training data	f	\N	\N
200	159	Test data	t	\N	\N
201	159	Validation data	f	\N	\N
202	160	Training data	f	\N	\N
203	160	Test data	f	\N	\N
204	160	Validation data	t	\N	\N
205	161	Curve Fitting	f	\N	\N
206	161	Understanding Data	t	\N	\N
207	161	Classification	f	\N	\N
208	161	Predictive Learning	f	\N	\N
209	162	$$d < d'$$	f	\N	\N
210	162	$$d > d'$$	t	\N	\N
211	162	$$d = d'$$	f	\N	\N
212	162	Any relation holds good	f	\N	\N
213	163	$$d < d'$$	f	\N	\N
214	163	$$d > d'$$	t	\N	\N
215	163	$$d = d'$$	f	\N	\N
216	163	Any relation holds good	f	\N	\N
217	164	$$\\frac{1}{n} \\sum ||g(X_i) - f(X_i)||^2$$	f	\N	\N
218	164	$$\\frac{1}{n} \\sum ||g(f(X_i)) - X_i||^2$$	t	\N	\N
219	164	$$\\frac{1}{n} \\sum ||f(g(X_i)) - X_i||^2$$	f	\N	\N
220	165	Reducing dimensionality	t	\N	\N
221	165	Grouping similar data	t	\N	\N
222	165	Density Estimation	t	\N	\N
223	166	$$\\{X_1, X_2, \\dots, X_n\\}$$	t	\N	\N
224	166	$$\\{(X_1, Y_1), (X_2, Y_2), \\dots, (X_n, Y_n)\\}$$	f	\N	\N
225	166	$$\\{(X_1, y_1), (X_2, y_2), \\dots, (X_n, y_n)\\}$$	f	\N	\N
226	167	Dimensionality reduction	f	\N	\N
227	167	Regression	f	\N	\N
228	167	Classification	f	\N	\N
229	167	Density estimation	t	\N	\N
230	168	$$\\frac{1}{n} \\sum \\log(P(X_i))$$	f	\N	\N
231	168	$$\\frac{1}{n} \\sum -\\log(P(X_i))$$	t	\N	\N
232	168	$$\\frac{1}{n} \\sum \\log(-P(X_i))$$	f	\N	\N
233	168	$$\\frac{1}{n} \\sum \\left(1 - \\log(-P(X_i))\\right)$$	f	\N	\N
234	169	Mean square error	f	\N	\N
235	169	Log-likelihood	f	\N	\N
236	169	Negative log-likelihood	t	\N	\N
237	169	Entropy	f	\N	\N
238	170	A model is a mathematical representation of reality.	f	\N	\N
239	170	A model is an exact representation of a system.	f	\N	\N
240	170	A model uses no assumptions.	f	\N	\N
241	170	only 1	t	\N	\N
242	170	only 2	f	\N	\N
243	171	Predicting the stock price of a company on a given day based on revenue growth and profit after tax.	t	\N	\N
244	171	Predicting the country that a person belongs to based on his physical features.	f	\N	\N
245	171	Predicting the animal present in a given image.	f	\N	\N
246	171	Predicting the topic of a given Wikipedia article.	f	\N	\N
247	172	The need to check for a long list of possible patterns that may be present.	f	\N	\N
248	172	Difficulty in maintaining the program containing the complex hard-coded rules.	f	\N	\N
249	172	The need to keep writing new rules as the spammers become innovative.	f	\N	\N
250	172	All of these.	t	\N	\N
251	173	are strictly integers.	f	\N	\N
252	173	always lie in the range $$[0, 1]$$.	f	\N	\N
253	173	are any real value.	t	\N	\N
254	173	are any imaginary value.	f	\N	\N
255	174	Find the gender of a person by analyzing writing style.	t	\N	\N
256	174	Predict the price of a car based on engine power, mileage etc.	f	\N	\N
257	174	Predict whether there will be abnormally heavy rainfall tomorrow or not based on previous data.	t	\N	\N
258	174	Predict the number of street accidents that will happen this month.	f	\N	\N
259	175	Predict the height of a person based on his weight.	t	\N	\N
260	175	Predict the country a person belongs to based on his linguistic features.	f	\N	\N
261	175	Predict whether the price of gold will increase tomorrow or not.	f	\N	\N
262	175	Predict whether a movie is comedy or tragedy based on its reviews.	f	\N	\N
263	176	Grouping tweets based on topic similarity	t	\N	\N
264	176	Making clusters of cells having similar appearance under microscope.	t	\N	\N
265	176	Checking whether an email is spam or not.	f	\N	\N
266	176	Identify the gender of online customers based on buying behaviour.	f	\N	\N
267	177	$$\\mathbb{1}(\\text{2 is even}) = 1$$	f	\N	\N
268	177	$$\\mathbb{1}(10 \\pmod 3 = 0) = 0$$	f	\N	\N
269	177	$$\\mathbb{1}(0.5 \\notin \\mathbb{R}) = 0$$	f	\N	\N
270	177	$$\\mathbb{1}(2 \\in \\{2,3,4\\}) = 0$$	t	\N	\N
271	178	$$f: \\mathbb{R}^d \\to \\mathbb{R}$$	f	\N	\N
272	178	$$f: \\mathbb{R}^d \\to \\{+1, -1\\}$$	t	\N	\N
273	178	$$f: \\mathbb{R}^d \\to \\mathbb{R}^{d'}$$	f	\N	\N
274	179	$$f: \\mathbb{R}^d \\to \\mathbb{R}^{d'} \\text{ where } d' < d \\text{ AND } g: \\mathbb{R}^{d'} \\to \\mathbb{R}^d \\text{ where } d' < d$$	t	\N	\N
275	179	$$f: \\mathbb{R}^d \\to \\mathbb{R}^{d'} \\text{ where } d' > d$$	f	\N	\N
276	179	$$g: \\mathbb{R}^{d'} \\to \\mathbb{R}^d \\text{ where } d' > d$$	f	\N	\N
277	180	Both (1) and (2) are suited for regression.	f	\N	\N
278	180	Both (1) and (2) are suited for classification.	f	\N	\N
279	180	Problem (1) is better suited for classification while (2) is better suited for regression.	t	\N	\N
280	180	Problem (2) is better suited for classification while (1) is better suited for regression.	f	\N	\N
281	183	let	f	\N	\N
282	183	var	f	\N	\N
283	183	const	f	\N	\N
284	183	All of the above	t	\N	\N
285	184	JavaScript is a statically typed language.	f	\N	\N
286	184	JavaScript is a dynamically typed language.	t	\N	\N
287	184	JavaScript is a weakly typed language.	t	\N	\N
288	184	JavaScript is a strongly typed language.	f	\N	\N
289	185	It is a forgiving language like HTML.	t	\N	\N
290	185	It inserts a semicolon after each statement automatically.	t	\N	\N
291	185	Blocks and functions both use { } for body contents.	t	\N	\N
292	185	Blocks use { } but functions use indentation for body contents.	f	\N	\N
293	186	undefined	f	\N	\N
294	186	Rohit	f	\N	\N
295	186	Mohit	t	\N	\N
296	186	\N	f	\N	\N
297	187	It will throw a TypeError.	f	\N	\N
298	187	Rohit	f	\N	\N
299	187	Mohit	t	\N	\N
300	187	undefined	f	\N	\N
301	188	undefined	f	\N	\N
302	188	Rohit	t	\N	\N
303	188	Mohit	f	\N	\N
304	188	\N	f	\N	\N
305	189	Rohit	t	\N	\N
306	189	Mohit	f	\N	\N
307	189	undefined	f	\N	\N
308	189	Syntax Error	f	\N	\N
309	190	'hello from setTimeOut one'\r\n'hello for main one'\r\n'hello from setTimeOut two'\r\n'hello from main two'	f	\N	\N
310	190	'hello for main one'\r\n'hello from setTimeOut one'\r\n'hello from main two'\r\n'hello from setTimeOut two'	f	\N	\N
311	190	'hello for main one'\r\n'hello from main two'\r\n'hello from setTimeOut two'\r\n'hello from setTimeOut one'	f	\N	\N
312	190	'hello for main one'\r\n'hello from main two'\r\n'hello from setTimeOut one'\r\n'hello from setTimeOut two'	t	\N	\N
313	191	red	f	\N	\N
314	191	black	f	\N	\N
315	191	yellow	t	\N	\N
316	191	None of the above	f	\N	\N
317	192	r	f	\N	\N
318	192	a	f	\N	\N
319	192	n	t	\N	\N
320	192	o	f	\N	\N
321	193	Text	t	\N	\N
322	193	Speech	t	\N	\N
323	193	Vision	t	\N	\N
324	194	(1) - (d), (2) - (b), (3) - (c), (4) - (a)	f	\N	\N
325	194	(1) - (d), (2) - (a), (3) - (c), (4) - (b)	t	\N	\N
326	195	Name of the customer	f	\N	\N
327	195	Age of the customer	t	\N	\N
328	195	Gender of the customer	t	\N	\N
329	195	Products that the customer has purchased in the past	t	\N	\N
330	195	Profiles of customers who have a similar purchase behaviour	t	\N	\N
331	195	The customer's PAN number	f	\N	\N
332	196	Films	t	\N	\N
333	196	None of the above	f	\N	\N
334	197	Yes	f	\N	\N
335	197	No	t	\N	\N
336	198	Machine learning is data-driven. The mere presence of data is not enough, what we do with the data matters. Machine learning is the science of learning from data. In the previous problem, no learning is involved.	t	\N	\N
337	198	The claim is completely correct. Any dataset can inherently be learned from.	f	\N	\N
338	199	Supervised learning	t	\N	\N
339	199	Regression	f	\N	\N
340	199	Unsupervised learning	t	\N	\N
341	199	Clustering	f	\N	\N
342	199	Sequential learning	t	\N	\N
343	199	Online learning	f	\N	\N
344	200	Given the image of a chest X-Ray, determine the presence or absence of a tumor.	t	\N	\N
345	200	Given a customer's financial background, determine if the customer can be given a loan or not.	t	\N	\N
346	200	Given the history of rainfall in a given region, predict the amount of rainfall for a given duration	f	\N	\N
347	200	Given a sound clip, determine the number of musical instruments that are present in it.	f	\N	\N
348	201	Regression	f	\N	\N
349	201	Binary classification (exactly 2 categories)	f	\N	\N
350	201	Multi-class classification (more than 2 categories)	t	\N	\N
351	201	This is not a supervised learning problem	f	\N	\N
352	202	Scenario-1: supervised learning\r\nScenario-2: unsupervised learning	t	\N	\N
353	202	Scenario-1: unsupervised learning\r\nScenario-2: supervised learning	f	\N	\N
354	203	True	f	\N	\N
355	203	False	t	\N	\N
356	204	$$n=4, d=5$$	f	\N	\N
357	204	$$n=5, d=4$$	t	\N	\N
358	204	$$n=d=4$$	f	\N	\N
359	204	$$n=d=5$$	f	\N	\N
360	205	$$ \\begin{bmatrix} 0 \\\\ 0 \\\\ 0 \\end{bmatrix} $$	f	\N	\N
361	205	$$ \\begin{bmatrix} 1 \\\\ 1 \\\\ 1 \\end{bmatrix} $$	f	\N	\N
362	205	$$ \\begin{bmatrix} -2 \\\\ -4 \\\\ 2 \\end{bmatrix} $$	t	\N	\N
363	205	$$ \\begin{bmatrix} 1 \\\\ 2 \\\\ -1 \\end{bmatrix} $$	t	\N	\N
364	207	0	f	\N	\N
365	207	1	f	\N	\N
366	207	2	t	\N	\N
367	207	infinite	f	\N	\N
368	208	$$ x^T w $$	f	\N	\N
369	208	$$ (x^T w)w $$	f	\N	\N
370	208	$$ \\left( \\frac{x^T w}{||w||^2} \\right) w $$	t	\N	\N
371	209	$$L_1$$, as it gives a better compression ratio	f	\N	\N
372	209	$$L_2$$, as it gives a better compression ratio	f	\N	\N
373	209	$$L_1$$, as it gives a smaller reconstruction error	t	\N	\N
374	209	$$L_2$$, as it gives a smaller reconstruction error	f	\N	\N
375	210	$$ \\frac{1}{n} \\sum_{i=1}^{n} ||x_i - (x_i^T w)w||^2 $$	t	\N	\N
376	210	$$ \\frac{1}{n} \\sum_{i=1}^{n} [x_i - (x_i^T w)w]^T [x_i - (x_i^T w)w] $$	t	\N	\N
377	210	$$ \\frac{1}{n} \\sum_{i=1}^{n} [x_i^T x_i - (x_i^T w)^2] $$	t	\N	\N
378	210	$$ \\frac{1}{n} \\sum_{i=1}^{n} (x_i^T w)^2 $$	f	\N	\N
379	210	$$ \\frac{1}{n} \\sum_{i=1}^{n} ||x_i||^2 $$	f	\N	\N
380	211	True	t	\N	\N
381	211	False	f	\N	\N
382	212	$$ \\max_{w, ||w||=1} \\frac{1}{n} \\sum_{i=1}^{n} (x_i^T w)^2 $$	t	\N	\N
383	212	$$ \\max_{w, ||w||=1} w^T \\left[ \\frac{1}{n} \\sum_{i=1}^{n} x_i x_i^T \\right] w $$	t	\N	\N
384	212	$$ \\min_{w, ||w||=1} \\frac{1}{n} \\sum_{i=1}^{n} (x_i^T w)^2 $$	f	\N	\N
385	212	$$ \\max_{w, ||w||=1} \\frac{1}{n} \\sum_{i=1}^{n} -(x_i^T w)^2 $$	f	\N	\N
386	213	$$ n \\times n $$	f	\N	\N
387	213	$$ d \\times d $$	t	\N	\N
388	213	$$ n \\times d $$	f	\N	\N
389	213	$$ d \\times n $$	f	\N	\N
390	214	It is the eigenvector corresponding to the minimum eigenvalue of the covariance matrix.	f	\N	\N
391	214	It could be any one of the eigenvectors of the covariance matrix. That is, every eigenvector is a solution of the optimization problem.	f	\N	\N
392	214	It is the eigenvector corresponding to the maximum eigenvalue of the covariance matrix.	t	\N	\N
393	215	Yes	t	\N	\N
394	215	No	f	\N	\N
395	216	$$ (x^T w)w $$	f	\N	\N
396	216	$$ x - w $$	f	\N	\N
397	216	$$ x - x^T w $$	f	\N	\N
398	216	$$ x - (x^T w)w $$	t	\N	\N
399	217	Only S1 is true	t	\N	\N
400	217	Only S2 is true	f	\N	\N
401	217	Both S1 and S2 are true	f	\N	\N
402	217	Both S1 and S2 are false	f	\N	\N
403	218	Yes	t	\N	\N
404	218	No	f	\N	\N
405	220	The vectors in $$B$$ are linearly independent	t	\N	\N
406	220	The vectors in $$B$$ span $$\\mathbb{R}^d$$	t	\N	\N
407	220	$$B$$ is a basis for $$\\mathbb{R}^d$$	t	\N	\N
408	220	$$w_i^T w_j = 0$$ for $$i \\neq j$$	t	\N	\N
409	220	$$w_i^T w_i = 1$$ for $$1 \\leq i \\leq d$$	t	\N	\N
410	222	The dataset is a subset of $$\\mathbb{R}^4$$	f	\N	\N
411	222	The dataset is a subset of a 4-dimensional linear subspace of $$\\mathbb{R}^{1000}$$	f	\N	\N
412	222	The dataset is a subset of a 4-dimensional linear subspace of $$\\mathbb{R}^{10}$$	t	\N	\N
413	223	It is the eigenvector corresponding to the $$k^{\\text{th}}$$ smallest eigenvalue of the covariance matrix.	f	\N	\N
414	223	It is the eigenvector corresponding to the $$k^{\\text{th}}$$ largest eigenvalue of the covariance matrix.	t	\N	\N
415	224	$$ 1 $$	f	\N	\N
416	224	$$ 0 $$	f	\N	\N
417	224	$$ \\lambda_k $$	t	\N	\N
418	224	$$ \\lambda_k^2 $$	f	\N	\N
419	225	Only S1 is true	f	\N	\N
420	225	Only S2 is true	f	\N	\N
421	225	Both S1 and S2 are true	t	\N	\N
422	225	Both S1 and S2 are false	f	\N	\N
423	227	$$L_1$$, as it gives a better compression ratio	f	\N	\N
424	227	$$L_2$$, as it gives a better compression ratio	f	\N	\N
425	227	$$L_1$$, as the variance of the dataset is higher along this direction	t	\N	\N
426	227	$$L_2$$, as the variance of the dataset is higher along this direction	f	\N	\N
427	227	$$L_1$$, as the variance of the dataset is lower along this direction	f	\N	\N
428	227	$$L_2$$, as the variance of the dataset is lower along this direction	f	\N	\N
429	228	4 KB	f	\N	\N
430	228	4 MB	f	\N	\N
431	228	40 MB	t	\N	\N
432	228	4 GB	f	\N	\N
433	230	$$ \\begin{bmatrix} 3 \\\\ 4 \\end{bmatrix} $$	f	\N	\N
434	230	$$ \\begin{bmatrix} 1/15 \\\\ 4/15 \\end{bmatrix} $$	f	\N	\N
435	230	$$ \\begin{bmatrix} 3/5 \\\\ 4/5 \\end{bmatrix} $$	t	\N	\N
436	230	$$ \\begin{bmatrix} 1 \\\\ 1 \\end{bmatrix} $$	f	\N	\N
437	231	$$ \\{0, 5, 10, 1/3\\} $$	t	\N	\N
438	231	$$ \\{0, 1, 2, 1/3\\} $$	f	\N	\N
439	231	$$ \\{0, 5, 10, 3\\} $$	f	\N	\N
440	231	$$ \\{0, 1, 10, 1/3\\} $$	f	\N	\N
441	232	$$ \\vec{OP} $$	f	\N	\N
442	232	$$ \\vec{OQ} $$	f	\N	\N
443	232	$$ \\vec{QP} $$	t	\N	\N
444	233	Yes	f	\N	\N
445	233	No	t	\N	\N
446	234	$$ |\\vec{QP}| < |\\vec{Q'P}| $$	f	\N	\N
447	234	$$ |\\vec{Q'P}| < |\\vec{QP}| $$	t	\N	\N
448	234	$$ |\\vec{QQ'}| = 0 $$	f	\N	\N
449	234	$$ |\\vec{QQ'}| > 0 $$	t	\N	\N
450	235	True	f	\N	\N
451	235	False	t	\N	\N
452	236	The dataset lies in a $$d$$-dimensional subspace of $$\\mathbb{R}^n$$	f	\N	\N
453	236	The dataset lies in a $$k$$-dimensional subspace of $$\\mathbb{R}^d$$	t	\N	\N
454	236	The dataset lies in a $$d$$-dimensional subspace of $$\\mathbb{R}^k$$	f	\N	\N
455	236	The dataset lies in a $$k$$-dimensional subspace of $$\\mathbb{R}^n$$	f	\N	\N
456	237	$$w_1$$	f	\N	\N
457	237	$$0$$	t	\N	\N
458	238	$$ \\frac{1}{n} X_1^T X_1 $$	t	\N	\N
459	238	$$ \\frac{1}{n} X_2^T X_2 $$	f	\N	\N
460	238	$$ \\frac{1}{n} X_1 X_1^T $$	f	\N	\N
461	238	$$ \\frac{1}{n} X_2 X_2^T $$	t	\N	\N
462	240	$$R_1: w^T x > 0$$	t	\N	\N
463	240	$$R_2: w^T x > 0$$	f	\N	\N
464	240	$$R_1: w^T x < 0$$	f	\N	\N
465	240	$$R_2: w^T x < 0$$	t	\N	\N
466	240	$$L: w^T x = 0$$	t	\N	\N
467	241	int	f	\N	\N
468	241	float	t	\N	\N
469	241	str	f	\N	\N
470	241	bool	f	\N	\N
471	242	str	f	\N	\N
472	242	bool	t	\N	\N
473	242	True	f	\N	\N
474	242	False	f	\N	\N
475	243	\N	f	code	(10^3) + (9^3) == (12^3) + (1^3) == 1729
476	243	\N	f	code	(10 ** 3) + (9 ** 3) = (12 ** 3) + (1 ** 3) = 1729
477	243	\N	f	code	(10 power 3) + (9 power 3) == (12 power 3) + (1 power 3) == 1729
478	243	\N	t	code	(10 ** 3) + (9 ** 3) == (12 ** 3) + (1 ** 3) == 1729
479	244	It is True if and only if both E_1 and E_2 have the same value.	f	\N	\N
480	244	It is False if and only if both E_1 and E_2 have the same value.	f	\N	\N
481	244	It is always True.	t	\N	\N
482	244	It is always False.	f	\N	\N
483	245	True	f	\N	\N
484	245	False	t	\N	\N
485	245	Cannot be determined	f	\N	\N
486	248	\N	t	code	name1 = input()\r\nname2 = input()\r\nprint(name1 < name2)
487	248	\N	f	code	name1 = input()\r\nname2 = input()\r\nprint(name1 > name2)
488	248	\N	t	code	print(input() < input())
489	248	\N	f	code	print(input() > input())
490	248	\N	t	code	name1 = input()\r\nname2 = input()\r\nresult = name1 < name2\r\nprint(result)
491	248	\N	f	code	name1 = input()\r\nname2 = input()\r\nresult = name1 > name2\r\nprint(result)
492	250	12	f	\N	\N
493	250	2	f	\N	\N
494	250	15 % 3 * 2 + 2	t	\N	\N
495	250	'15 % 3 * 2 + 2'	f	\N	\N
496	251	a + 'b' + c + '' + d	t	\N	\N
497	251	"a + 'b' + c + '' + d"	f	\N	\N
498	251	a + b + c + '' + d	f	\N	\N
499	251	a + '''b''' + c + '''' + d	f	\N	\N
500	252	\N	f	code	print(1 2 3 4 5)
501	252	\N	t	code	print('1 2 3 4 5') # there is a space between consecutive numbers
502	252	\N	f	code	print(1)\r\nprint(2)\r\nprint(3)\r\nprint(4)\r\nprint(5)
503	252	\N	t	code	print(1, 2, 3, 4, 5)
504	253	1 - (A), 2 - (C), 3 - (B), 4 - (D), 5 - (A)	f	\N	\N
505	253	1 - (B), 2 - (C), 3 - (A), 4 - (D), 5 - (A)	t	\N	\N
506	253	1 - (A), 2 - (C), 3 - (B), 4 - (D), 5 - (B)	f	\N	\N
507	253	1 - (B), 2 - (C), 3 - (A), 4 - (D), 5 - (B)	f	\N	\N
508	254	\N	f	code	word[0] + word[1]
509	254	\N	t	code	word[0] + word[-1]
510	254	\N	t	code	word[0] + word[len(word) - 1]
511	254	\N	f	code	word[-1] + word[len(word)]
512	255	11	f	\N	\N
513	255	11.0	t	\N	\N
514	255	33	f	\N	\N
515	255	33.0	f	\N	\N
516	258	a_	t	\N	\N
517	258	_a	t	\N	\N
518	258	1a	f	\N	\N
519	258	a variable	f	\N	\N
520	258	a_variable	t	\N	\N
525	260	\N	t	code	x == y == z
526	260	\N	f	code	x == y == z == a
527	260	\N	f	code	x == y == z == b
528	260	\N	t	code	x == y == z == c
529	261	\N	f	code	a\r\na
530	261	\N	f	code	a + 1\r\na + 1
531	261	\N	f	code	a - 1\r\na - 1
532	261	\N	f	code	a - 1\r\n-a
533	261	\N	f	code	a\r\n-a + 1
534	261	\N	t	code	a\r\n-a
535	262	Yes	t	\N	\N
536	262	No	f	\N	\N
537	263	All three blocks are equivalent to each other.	f	\N	\N
538	263	Exactly two of these three blocks are equivalent to each other.	f	\N	\N
539	263	Blocks 1 and 2 print the same output when E evaluates to True.	f	\N	\N
540	263	Blocks 1 and 2 print the same output when E evaluates to False.	t	\N	\N
541	263	Blocks 2 and 3 print the same output when E evaluates to True.	t	\N	\N
542	264	The value of variable x is independent of the value of bool_var.	t	\N	\N
543	264	The value of variable x is dependent on the value of boon_var.	f	\N	\N
544	264	Line-5 is never executed.	t	\N	\N
545	264	The variable x is updated exactly two times.	f	\N	\N
546	265	When all three Boolean variables are True.	f	\N	\N
547	265	When all three Boolean variables are False.	t	\N	\N
548	265	When at least one of the three Boolean variables is True.	f	\N	\N
549	265	When at least one of the three Boolean variables is False.	f	\N	\N
550	265	This code will never throw an error.	f	\N	\N
551	267	\N	f	code	print(\\)
552	267	\N	f	code	print('\\')
553	267	\N	t	code	print('\\\\')
554	267	\N	f	code	print("\\")
555	268	Neeraj	t	\N	\N
556	268	Mirabai	t	\N	\N
557	268	Sindhu	t	\N	\N
558	268	X AE A-12	f	\N	\N
559	268	Rohit Sharma	f	\N	\N
560	269	abcdefghij	f	\N	\N
561	269	abcde	f	\N	\N
562	269	acegi	t	\N	\N
563	269	bdfhj	f	\N	\N
564	270	\N	f	code	1234\r\n1234\r\n1234\r\n1234
565	270	\N	t	code	1\r\n2\r\n3\r\n4
566	270	\N	f	code	1\r\n1\r\n1\r\n1
567	270	\N	f	code	4\r\n4\r\n4\r\n4
568	271	tacit	t	\N	\N
569	271	trumpet	t	\N	\N
570	271	ease	t	\N	\N
571	271	TrumpeT	f	\N	\N
572	271	TaciT	f	\N	\N
573	272	A word is termed valid if it begins with a lower case letter.	f	\N	\N
574	272	A word is termed valid if its first and last characters are the same.	f	\N	\N
575	272	A word is termed valid if it begins with a lower case letter AND its first and last characters are the same.	t	\N	\N
576	272	A word is termed valid if it begins with a lower case letter OR its first and last characters are the same.	f	\N	\N
577	274	\N	f	code	num = int(input())\r\nfirst, middle, last = num[0], num[1], num[2]\r\nif first + last == middle:\r\n    print('sandwich')\r\nelse:\r\n    print('plain')
578	274	\N	f	code	num = input()\r\nfirst, middle, last = num[0], num[1], num[2]\r\nif first + last == middle:\r\n    print('sandwich')\r\nelse:\r\n    print('plain')
579	274	\N	t	code	num = input()\r\nfirst, middle, last = int(num[0]), int(num[1]), int(num[2])\r\nif first + last == middle:\r\n    print('sandwich')\r\nelse:\r\n    print('plain')
580	274	\N	f	code	num = int(input())\r\nfirst, middle, last = int(num[0]), int(num[1]), int(num[2])\r\nif first + last == middle:\r\n    print('sandwich')\r\nelse:\r\n    print('plain')
522	259	The two lines are always different.	f	\N	\N
524	259	None of the above	f	\N	\N
581	277	When any two among x, y and z are equal	f	\N	\N
582	277	When all the values of x, y and z are equal	f	\N	\N
583	277	When any one among x, y and z is zero	f	\N	\N
584	277	When all the values of x, y and z are zeros	t	\N	\N
585	278	True	f	\N	\N
586	278	False	t	\N	\N
587	279	\N	f	code	sentence = input()\r\nspace = ' ' # there is a single space between the quotes\r\nnum_words = sentence.count(space)\r\nprint(num_words)
588	279	\N	t	code	sentence = input()\r\nspace = ' ' # there is a single space between the quotes\r\nnum_words = sentence.count(space) + 1\r\nprint(num_words)
589	279	\N	f	code	sentence = int(input())\r\nspace = ' ' # there is a single space between the quotes\r\nnum_words = sentence.count(space)\r\nprint(num_words)
590	279	\N	f	code	sentence = input()\r\nnum_words = len(sentence)\r\nprint(num_words)
591	280	\N	f	text	ABD\r\nXYZ\r\nMR\r\nFNAME LNAME\r\n999
592	280	\N	f	text	ABC\r\nXYZ\r\nMRS\r\nFNAME LNAME\r\n999
593	280	\N	t	text	ABC\r\nXYZ\r\nMR\r\nfname lname\r\n999
594	280	\N	f	text	ABC\r\nMR\r\nXYZ\r\nFNAME LNAME\r\n999
595	281	(a{b[c]})	t	\N	\N
596	281	abcd	t	\N	\N
597	281	)(][}{	t	\N	\N
598	281	a(db]	f	\N	\N
599	108	[]	f	\N	\N
600	108	Error	f	\N	\N
601	108	[5, 22, 55, 75]	f	\N	\N
602	108	[22, 5, 55, 75]	t	\N	\N
603	133	Abhi	f	\N	\N
604	133	Akshay	t	\N	\N
605	133	undefined	f	\N	\N
606	133	ReferenceError	f	\N	\N
607	132	Abhi	t	\N	\N
608	132	Akshay	f	\N	\N
609	132	Undefined	f	\N	\N
610	132	ReferenceError	f	\N	\N
611	134	100	f	\N	\N
612	134	120	t	\N	\N
613	134	140	f	\N	\N
614	134	160	f	\N	\N
615	282	6	f	\N	\N
616	282	5	f	\N	\N
617	282	8	t	\N	\N
618	282	None of the above	f	\N	\N
619	135	3	f	\N	\N
620	135	5	f	\N	\N
621	135	7	t	\N	\N
622	135	15	f	\N	\N
623	136	Undefined	f	\N	\N
624	136	Modern Application Development 2	t	\N	\N
625	136	Will throw syntax error	f	\N	\N
626	136	None of the above	f	\N	\N
631	138	Application	f	\N	\N
632	138	Programming	t	\N	\N
633	138	Interface	f	\N	\N
634	138	A	f	\N	\N
639	1	The residue is equal to the zero vector.	f	\N	\N
640	1	The residue is equal to the vector $x$.	t	\N	\N
641	1	The projection is the zero vector.	t	\N	\N
642	1	The projection is equal to the vector $x$.	f	\N	\N
643	4	$P:(-ve,-ve)$	f	\N	\N
644	4	$P:(-ve,+ve)$	t	\N	\N
645	4	$Q:(+ve,+ve)$	f	\N	\N
646	4	$Q:(+ve,-ve)$	t	\N	\N
647	6	\N	f	image	img_002.png
648	6	\N	t	image	img_003.png
649	9	Statement-1	f	\N	\N
650	9	Statement-2	f	\N	\N
651	9	Statement-3	f	\N	\N
652	9	Statement-4	f	\N	\N
653	9	None of these statements are true.	t	\N	\N
654	11	$\\begin{bmatrix} 3.5 \\\\ 3.5 \\end{bmatrix}$	f	\N	\N
655	11	$\\begin{bmatrix} -1.5 \\\\ 1.5 \\end{bmatrix}$	t	\N	\N
656	11	$\\begin{bmatrix} 2 \\\\ 5 \\end{bmatrix}$	f	\N	\N
657	11	$\\begin{bmatrix} 1 \\\\ 4 \\end{bmatrix}$	f	\N	\N
658	5	$\\begin{bmatrix} 4.5 & -0.5 \\\\ -0.5 & 0.25 \\end{bmatrix}$	t	\N	\N
659	5	$\\begin{bmatrix} 36 & -4 \\\\ -4 & 2 \\end{bmatrix}$	f	\N	\N
660	5	$\\begin{bmatrix} 1 & 0 \\\\ 0 & 1 \\end{bmatrix}$	f	\N	\N
661	5	$\\begin{bmatrix} 1 & 1 \\\\ 1 & 1 \\end{bmatrix}$	f	\N	\N
662	10	Yes	t	\N	\N
663	10	No	f	\N	\N
664	13	We cannot run the PCA as $k$ is not a valid kernel.	f	\N	\N
665	13	It will be the same as PCA with no kernel.	t	\N	\N
666	13	It will be the same as the polynomial transformation of degree 2 and then run the PCA.	f	\N	\N
667	13	It will be the same as the polynomial transformation of degree 3 and then run the PCA.	f	\N	\N
668	14	The transformed data points will lie on a 5-dimensional subspace of $\\mathbb{R}^6$.	t	\N	\N
669	14	The transformed data points will lie on a 6-dimensional subspace of $\\mathbb{R}^{10}$	f	\N	\N
670	14	There will be some $w \\in \\mathbb{R}^6$ that all of the data points are orthogonal to.	t	\N	\N
671	14	There will be some $w \\in \\mathbb{R}^{10}$ that all of the data points are orthogonal to.	f	\N	\N
672	15	$\\begin{bmatrix} 1 & 8 \\\\ 8 & -1 \\end{bmatrix}$	t	\N	\N
673	15	$\\begin{bmatrix} 1 & 8 \\\\ 8 & 1 \\end{bmatrix}$	t	\N	\N
674	15	$\\begin{bmatrix} 1 & -8 \\\\ 8 & 1 \\end{bmatrix}$	t	\N	\N
675	15	$\\begin{bmatrix} 1 & 0 \\\\ 0 & 1 \\end{bmatrix}$	f	\N	\N
676	16	Yes	t	\N	\N
677	16	No	f	\N	\N
678	17	$2 \\times 2$	f	\N	\N
679	17	$4 \\times 4$	t	\N	\N
680	17	$6 \\times 6$	f	\N	\N
681	17	None of the above	f	\N	\N
682	18	-4	f	\N	\N
683	18	16	t	\N	\N
684	18	13	f	\N	\N
685	18	196	f	\N	\N
686	20	$x_i^T \\alpha_k$	f	\N	\N
687	20	$\\frac{x_i^T \\alpha_k}{\\sqrt{\\lambda}}$	f	\N	\N
688	20	$\\frac{x_i^T X \\alpha_k}{\\sqrt{\\lambda}}$	t	\N	\N
689	20	$\\frac{x_i^T X \\alpha_k}{\\sqrt{n\\lambda}}$	f	\N	\N
690	21	Yes	t	\N	\N
691	21	No	f	\N	\N
692	22	Statement 1 is correct but statement 2 is incorrect.	f	\N	\N
693	22	Statement 1 is incorrect but statement 2 is correct.	f	\N	\N
694	22	Both statements are correct.	t	\N	\N
695	22	Both statements are incorrect.	f	\N	\N
696	23	$(x_1 x_2 + 1)^3$	t	\N	\N
697	23	$(x_2 x_1 + 1)^3$	t	\N	\N
698	23	$(x_1 x_2 + 1)^4$	f	\N	\N
699	23	$\\phi(x_2)^T \\phi(x_1)$	t	\N	\N
700	24	$2, 5, 7$	f	\N	\N
701	24	$2d, 5d, 7d$	f	\N	\N
636	61	Red, 50px, 50px	t	\N	\N
637	61	Green, 50px, 100px	f	\N	\N
638	61	Green, 50px, 50px	f	\N	\N
627	137	500px	t	\N	\N
628	137	1000px	f	\N	\N
629	137	0px	f	\N	\N
630	137	None of the above	f	\N	\N
702	24	$2n, 5n, 7n$	t	\N	\N
703	24	Can not be determined	f	\N	\N
704	27	$4$	f	\N	\N
705	27	$\\frac{1}{\\sqrt{51}}$	f	\N	\N
706	27	$\\frac{1}{2\\sqrt{51}}$	t	\N	\N
707	27	$\\left[ \\frac{1}{\\sqrt{51}}, \\frac{3}{\\sqrt{51}}, \\frac{4}{\\sqrt{51}}, \\frac{5}{\\sqrt{51}} \\right]^T$	f	\N	\N
708	27	$\\left[ \\frac{1}{2\\sqrt{51}}, \\frac{3}{2\\sqrt{51}}, \\frac{4}{2\\sqrt{51}}, \\frac{5}{2\\sqrt{51}} \\right]^T$	f	\N	\N
709	29	Yes	t	\N	\N
710	29	No	f	\N	\N
711	30	Standard PCA	f	\N	\N
712	30	Kernel PCA with a polynomial kernel of degree 2	f	\N	\N
713	30	Kernel PCA with a polynomial kernel of degree 3	t	\N	\N
714	30	Kernel PCA with a polynomial kernel of degree 4	f	\N	\N
715	31	Strategy 1	f	\N	\N
716	31	Strategy 2	t	\N	\N
717	31	Both strategies are the same	f	\N	\N
718	33	$10$	f	\N	\N
719	33	$40$	f	\N	\N
720	33	$\\infty$	t	\N	\N
721	33	Can not be determined	f	\N	\N
722	66	1	f	\N	\N
723	66	2	f	\N	\N
724	66	3	t	\N	\N
725	66	4	f	\N	\N
726	67	abhi	f	\N	\N
727	67	alt	f	\N	\N
728	67	Reference Error	t	\N	\N
729	67	None of the above	f	\N	\N
730	68	[ 'string', 'boolean', 'number', 'function' ]	t	\N	\N
731	68	['iitmonline', true, 3, (a, b) => a + b]	f	\N	\N
732	68	[object, object, object, object]	f	\N	\N
733	68	None of the above	f	\N	\N
734	69	[NaN, NaN, 9, NaN]	f	\N	\N
735	69	[NaN, 1, 9, NaN]	t	\N	\N
736	69	[1, 1, 9, NaN]	f	\N	\N
737	69	None of the above	f	\N	\N
738	70	It will throw syntax error	f	\N	\N
739	70	Apple is red and undefined	f	\N	\N
740	70	Undefined is undefined and Spherical	f	\N	\N
741	70	Apple is red and Spherical	t	\N	\N
742	71	Bowler {\r\n  name: 'Jasprit Bumrah',\r\n  team: 'Indian Cricket Team',\r\n  nationality: 'Indian',\r\n  role: 'Bowler',\r\n  wicket: 101,\r\n  average: 22.79\r\n}	t	\N	\N
743	71	Bowler {\r\n  name: 'Jasprit Bumrah',\r\n  team: undefined,\r\n  nationality: undefined,\r\n  role: 'Bowler',\r\n  wicket: 101,\r\n  average: 22.79\r\n}	f	\N	\N
744	71	Bowler {\r\n  name: undefined,\r\n  team: undefined,\r\n  nationality: undefined,\r\n  role: 'Bowler',\r\n  wicket: 101,\r\n  average: 22.79\r\n}	f	\N	\N
745	71	None of the above	f	\N	\N
746	72	undefined from undefined is a Batsman	f	\N	\N
747	72	Rohit from Indian Cricket Team is an undefined	f	\N	\N
748	72	undefined from Indian Cricket Team is a Batsman	f	\N	\N
749	72	Rohit from Indian Cricket Team is a Batsman	t	\N	\N
750	73	[17, NaN, 29]	f	\N	\N
751	73	[17, 20, 29]	t	\N	\N
752	73	[NaN, 20, 29]	f	\N	\N
753	73	Syntax error	f	\N	\N
754	74	Mishra	f	\N	\N
755	74	Mourya	t	\N	\N
756	74	Syntax Error	f	\N	\N
757	74	None of the above	f	\N	\N
758	75	Code snippet 1	t	\N	\N
759	75	Code snippet 2	f	\N	\N
760	75	Both Code snippets 1 and 2	f	\N	\N
761	75	None of the above	f	\N	\N
762	34	3, 5, 1, 4, 2	f	\N	\N
763	34	5, 3, 1, 2, 4	f	\N	\N
764	34	5, 3, 1, 4, 2	t	\N	\N
765	34	3, 5, 2, 4, 1	f	\N	\N
766	34	None of these	f	\N	\N
767	35	$F(z_1^{t+1},z_2^{t+1},\\dots,z_n^{t+1}) > F(z_1^t,z_2^t,\\dots,z_n^t)$	f	\N	\N
768	35	$F(z_1^{t+1},z_2^{t+1},\\dots,z_n^{t+1}) < F(z_1^t,z_2^t,\\dots,z_n^t)$	t	\N	\N
769	35	$F(z_1^{t+1},z_2^{t+1},\\dots,z_n^{t+1}) = F(z_1^t,z_2^t,\\dots,z_n^t)$	f	\N	\N
770	36	Perpendicular to the line joining $\\mu_1$ and $\\mu_2$ and at the point $\\frac{(\\mu_1+\\mu_2)^2}{2}$	f	\N	\N
771	36	Parallel to the line joining $\\mu_1$ and $\\mu_2$ and at the point $\\frac{(\\mu_1+\\mu_2)^2}{2}$	f	\N	\N
772	36	Perpendicular to the line joining $\\mu_1$ and $\\mu_2$ and at the point $\\frac{\\mu_1+\\mu_2}{2}$	t	\N	\N
773	36	Parallel to the line joining $\\mu_1$ and $\\mu_2$ and at the point $\\frac{\\mu_1+\\mu_2}{2}$	f	\N	\N
774	37	a)	f	image	km2.png
775	37	b)	f	image	km3.png
776	37	c) Depends on cluster center initializations and the distance between the two lines.	t	\N	\N
777	38	Any point out of of $x_1, x_2, x_3, x_4, x_5$ may be chosen uniformly at random as next mean.	f	\N	\N
778	38	Certainly $x_3$ will be chosen as its distance from closest mean is largest.	f	\N	\N
779	38	$x_3$ will be chosen with the highest probability, but we are not sure whether this point will definitely be chosen.	t	\N	\N
780	39	The partition configurations can not repeat themselves.	t	\N	\N
781	39	After doing the reassignments, we might get the same partition configuration again.	f	\N	\N
782	39	Objective function after making the re-assignments strictly reduces.	t	\N	\N
783	39	Objective function after making the re-assignments may increase.	f	\N	\N
784	39	Change of value of objective function indicates that the partition configuration has changed.	t	\N	\N
785	39	For partitioning $n$ data points across $k$ partitions, Lloyd's algorithm takes $k^n$ iterations to converge.	f	\N	\N
786	40	1	t	\N	\N
787	40	10	f	\N	\N
788	40	100	f	\N	\N
789	40	Insufficient information. Depends on data.	f	\N	\N
790	41	100	f	\N	\N
791	41	0	t	\N	\N
792	41	100*100	f	\N	\N
793	42	In k-means algorithm, all cluster initializations lead to the same result.	f	\N	\N
794	42	One initialization might get stuck in local minima, while another may lead to global minima.	t	\N	\N
795	42	One initialization may converge while another may not.	f	\N	\N
796	42	The initialization of cluster centres may affect the number of iterations K-means takes to converge.	t	\N	\N
797	43	Yes	t	\N	\N
798	43	No	f	\N	\N
799	44	$\\mathbb{R}$	f	\N	\N
800	44	$\\mathbb{R}^+$	f	\N	\N
801	44	Both $\\mathbb{R}^+$ and $\\mathbb{R}^-$	f	\N	\N
802	44	$\\mathbb{R}^3$	t	\N	\N
803	45	$\\frac{1}{n}\\sum_{i=1}^n(f(x_i)-y_i)^2$	f	\N	\N
804	45	$\\frac{1}{n}\\sum_{i=1}^n|f(x_i)-y_i|$	f	\N	\N
805	45	$\\frac{1}{n}\\sum_{i=1}^n\\mathbb{1}(f(x_i)\\neq y_i)$	t	\N	\N
1209	358	$[-1, 1, -3]$	f	\N	\N
1210	358	$[1, 2, 1]$	f	\N	\N
806	46	Predicting the amount of rainfall in May 2022 in North India based on precipitation data of the year 2021.	f	\N	\N
807	46	Predicting the price of a land based on its area and distance from the market.	f	\N	\N
808	46	Predicting whether an email is spam or not.	t	\N	\N
809	46	Predicting the number of Covid cases on a given day based on previous month data.	f	\N	\N
810	47	$\\mathbb{1}(355\\%2 = 1) = 1$	f	\N	\N
811	47	$\\mathbb{1}(788\\%2 = 1) = 0$	f	\N	\N
812	47	$\\mathbb{1}(355\\%2 = 0) = 1$	t	\N	\N
813	47	$\\mathbb{1}(788\\%2 = 0) = 1$	f	\N	\N
814	48	Unsupervised machine learning helps you to find different kinds of unknown patterns in data.	f	\N	\N
815	48	Regression and classification are two types of supervised machine learning techniques while clustering and density estimation are two types of unsupervised learning.	f	\N	\N
816	48	In unsupervised learning model, the data contains both input and output variables while in supervised learning model, the data contains only input data	t	\N	\N
817	49	is discrete	f	\N	\N
818	49	is continuous and always within a finite range.	f	\N	\N
819	49	is continuous with any range.	t	\N	\N
820	49	may be discrete or continuous.	f	\N	\N
821	50	Making different groups of customers based on their purchase history.	f	\N	\N
822	50	Predicting whether a loan client may default or not based on previous credit history.	t	\N	\N
823	50	Grouping similar Wikipedia articles as per their content.	f	\N	\N
824	50	Estimating the revenue of a company for a given year based on number of items sold.	t	\N	\N
825	51	Classification	f	\N	\N
826	51	Regression	t	\N	\N
827	51	Density Estimation	f	\N	\N
828	51	Dimensionality Reduction	f	\N	\N
829	52	Test set; Validation set; training set	f	\N	\N
830	52	Training set; Test set; Validation set	f	\N	\N
831	52	Training set; Validation set; Test set	t	\N	\N
832	52	Test set; Training set; Validation set	f	\N	\N
833	53	(1, 1)	t	\N	\N
834	53	(1, 2)	f	\N	\N
835	53	(2, 1)	f	\N	\N
836	53	(2, 2)	f	\N	\N
837	54	Dimensionality Reduction, Regression, Classification, Density Estimation	f	\N	\N
838	54	Dimensionality Reduction, Classification, Density Estimation, Regression	f	\N	\N
839	54	Density Estimation, Dimensionality Reduction, Regression, Classification	t	\N	\N
840	54	Classification, Density Estimation, Dimensionality Reduction, Regression	f	\N	\N
841	54	Classification, Dimensionality Reduction, Regression, Density Estimation	f	\N	\N
842	77	$x^Tx$	f	\N	\N
843	77	$||x||^2$	f	\N	\N
844	77	$\\sum_{i=1}^dx_i^2$	f	\N	\N
845	77	$xx^T$	t	\N	\N
846	78	$f(x)$ is continuous at $x=3$.	f	\N	\N
847	78	$f(x)$ is not continuous at $x=3$.	t	\N	\N
848	78	$f(x)$ is differentiable at $x=3$.	f	\N	\N
849	78	$f(x)$ is not differentiable at $x=3$.	t	\N	\N
850	81	$[2, 3, 5]$ and $[-2, 3, -1]$	t	\N	\N
851	89	$\\frac{1}{x-1}$	t	\N	\N
852	89	$\\frac{x^2-1}{x-1}$	t	\N	\N
853	89	$\\text{sign}(x-2)$	f	\N	\N
854	89	$\\sin(x)$	t	\N	\N
855	81	$[1, 0, 1]$ and $[0, 1, 1]$	f	\N	\N
856	81	$[2, 3, 5]$ and $[-2, 3, -5]$	f	\N	\N
857	81	$[0, 1, 0]$ and $[0, 0, 1]$	t	\N	\N
858	81	$[2, -3, 5]$ and $[-2, 3, -5]$	f	\N	\N
859	81	$[1, 0, 0]$ and $[0, 1, 0]$	t	\N	\N
860	82	$4x+4y-8$	f	\N	\N
861	82	$12x+12y-32$	t	\N	\N
862	82	$12x+4y-8$	f	\N	\N
863	82	$12x+12y+32$	f	\N	\N
864	83	$[12, 4]$	t	\N	\N
865	83	$[4, 12]$	f	\N	\N
866	83	$[1, 4]$	f	\N	\N
867	83	$[4, 1]$	f	\N	\N
868	84	$[1, 2, 3]$	f	\N	\N
869	84	$[-1, 2, 3]$	f	\N	\N
870	84	$[0, 2, 3]$	t	\N	\N
871	84	$[2, 0, 3]$	f	\N	\N
872	86	$\\begin{bmatrix} \\frac{2}{\\sqrt{20}}, & 0, & \\frac{4}{\\sqrt{20}} \\end{bmatrix}$	t	\N	\N
873	86	$\\begin{bmatrix} \\frac{1}{\\sqrt{29}}, & 0, & \\frac{1}{\\sqrt{29}} \\end{bmatrix}$	f	\N	\N
874	86	$\\begin{bmatrix} \\frac{-2}{\\sqrt{29}}, & 0, & \\frac{4}{\\sqrt{29}} \\end{bmatrix}$	f	\N	\N
875	86	$\\begin{bmatrix} \\frac{2}{\\sqrt{20}}, & 0, & \\frac{-4}{\\sqrt{20}} \\end{bmatrix}$	f	\N	\N
876	88	$[1,2,3]+\\alpha[-6,-6,3]$	f	\N	\N
877	88	$[7,8,9]+\\alpha[-6,-6,3]$	f	\N	\N
878	88	$[1,2,3]+\\alpha[6,6,3]$	f	\N	\N
879	88	$[7,8,6]+\\alpha[6,6,3]$	f	\N	\N
880	88	$[7,8,6]+\\alpha[1,2,3]$	t	\N	\N
881	88	$[1,2,3]+\\alpha[7,8,6]$	f	\N	\N
882	90	(i) only	f	\N	\N
883	90	(ii) only	f	\N	\N
884	90	(iii) only	f	\N	\N
885	90	(iv) only	f	\N	\N
886	90	(i) and (ii)	t	\N	\N
887	90	(iii) and (iv)	f	\N	\N
888	91	True	t	\N	\N
889	91	False	f	\N	\N
890	92	$A^C=[10,30] \\cup [50,100]$	t	\N	\N
891	92	$A^C=[10,30) \\cup (50,100]$	f	\N	\N
892	92	$A \\cup B=[30,90]$	f	\N	\N
893	92	$A \\cap B=\\emptyset$	t	\N	\N
894	92	$A \\cap B=\\{50\\}$	f	\N	\N
895	92	$A^C \\cap B^C=[10,30) \\cup [91,100]$	f	\N	\N
896	93	Only (i) and (ii)	f	\N	\N
897	93	Only (ii) and (iii)	f	\N	\N
898	93	Only (i) and (iii)	f	\N	\N
899	93	(i), (ii) and (iii)	t	\N	\N
900	94	$1+x$	f	\N	\N
901	94	$1-x$	f	\N	\N
902	94	$x-1$	f	\N	\N
903	94	$x$	t	\N	\N
904	96	Yes	t	\N	\N
905	96	No	f	\N	\N
906	100	$1$	f	\N	\N
907	100	$0$	f	\N	\N
908	100	$0.019$	f	\N	\N
909	100	$1.019$	t	\N	\N
910	101	$2x+2y+2$	f	\N	\N
911	101	$2x+2y-2$	t	\N	\N
912	101	$2x+2y+1$	f	\N	\N
913	101	$2x+2y-1$	f	\N	\N
914	102	$[1, 6]$	f	\N	\N
915	102	$[6, 1]$	t	\N	\N
916	102	$[1, 3]$	f	\N	\N
917	102	$[3, 1]$	f	\N	\N
918	104	$\\begin{bmatrix} \\frac{2}{\\sqrt{29}}, & \\frac{3}{\\sqrt{29}}, & \\frac{4}{\\sqrt{29}} \\end{bmatrix}$	t	\N	\N
919	104	$\\begin{bmatrix} \\frac{-2}{\\sqrt{29}}, & \\frac{3}{\\sqrt{29}}, & \\frac{4}{\\sqrt{29}} \\end{bmatrix}$	f	\N	\N
920	104	$\\begin{bmatrix} \\frac{-2}{\\sqrt{29}}, & \\frac{-3}{\\sqrt{29}}, & \\frac{4}{\\sqrt{29}} \\end{bmatrix}$	f	\N	\N
921	104	$\\begin{bmatrix} \\frac{2}{\\sqrt{29}}, & \\frac{-3}{\\sqrt{29}}, & \\frac{4}{\\sqrt{29}} \\end{bmatrix}$	f	\N	\N
922	106	(i)	f	\N	\N
923	106	(i) and (ii)	t	\N	\N
924	106	(iii) and (iv)	f	\N	\N
925	106	(i) and (iii)	f	\N	\N
926	106	(ii) and (iv)	f	\N	\N
927	107	$a^Tb \\geq ||a||*||b||$	f	\N	\N
928	107	$a^Tb \\leq ||a||*||b||$	f	\N	\N
929	107	$a^Tb = ||a||*||b||$	f	\N	\N
930	107	$a^Tb = -||a||*||b||$	t	\N	\N
1066	317	$\\text{Span } \\left\\{ \\begin{bmatrix} 1 \\\\ 0 \\\\ 9 \\\\ 2 \\end{bmatrix}, \\begin{bmatrix} 0 \\\\ 1 \\\\ -3 \\\\ 1 \\end{bmatrix} \\right\\}$	t	\N	\N
1067	317	$\\text{Span } \\left\\{ \\begin{bmatrix} 9 \\\\ 3 \\\\ 1 \\\\ 0 \\end{bmatrix}, \\begin{bmatrix} -2 \\\\ 1 \\\\ 0 \\\\ 1 \\end{bmatrix} \\right\\}$	f	\N	\N
1068	317	$\\text{Span } \\left\\{ \\begin{bmatrix} 1 \\\\ 0 \\\\ -9 \\\\ 0 \\end{bmatrix}, \\begin{bmatrix} 0 \\\\ 1 \\\\ 0 \\\\ 1 \\end{bmatrix} \\right\\}$	f	\N	\N
1069	317	$\\text{Span } \\left\\{ \\begin{bmatrix} 0 \\\\ 3 \\\\ 1 \\\\ 0 \\end{bmatrix}, \\begin{bmatrix} 3 \\\\ -1 \\\\ 0 \\\\ 1 \\end{bmatrix} \\right\\}$	f	\N	\N
1070	318	$\\begin{bmatrix} \\frac{1}{3} & \\frac{1}{3} & \\frac{1}{3} \\\\ \\frac{1}{3} & \\frac{1}{3} & \\frac{1}{3} \\\\ \\frac{1}{3} & \\frac{1}{3} & \\frac{1}{3} \\end{bmatrix}$	t	\N	\N
1071	318	$\\begin{bmatrix} \\frac{1}{3} & -\\frac{1}{3} & \\frac{1}{3} \\\\ -\\frac{1}{3} & \\frac{1}{3} & -\\frac{1}{3} \\\\ \\frac{1}{3} & -\\frac{1}{3} & \\frac{1}{3} \\end{bmatrix}$	f	\N	\N
1072	318	$\\begin{bmatrix} -\\frac{1}{3} & \\frac{1}{3} & -\\frac{1}{3} \\\\ \\frac{1}{3} & -\\frac{1}{3} & \\frac{1}{3} \\\\ -\\frac{1}{3} & \\frac{1}{3} & -\\frac{1}{3} \\end{bmatrix}$	f	\N	\N
1073	318	$\\begin{bmatrix} -\\frac{1}{3} & \\frac{1}{3} & \\frac{1}{3} \\\\ \\frac{1}{3} & -\\frac{1}{3} & \\frac{1}{3} \\\\ \\frac{1}{3} & \\frac{1}{3} & -\\frac{1}{3} \\end{bmatrix}$	f	\N	\N
1074	319	$\\begin{bmatrix} \\frac{3}{14} \\\\ -\\frac{6}{14} \\\\ -\\frac{9}{14} \\end{bmatrix}$	t	\N	\N
1075	319	$\\begin{bmatrix} \\frac{3}{14} \\\\ \\frac{6}{14} \\\\ \\frac{9}{14} \\end{bmatrix}$	f	\N	\N
1076	319	$\\begin{bmatrix} -\\frac{3}{14} \\\\ -\\frac{6}{14} \\\\ -\\frac{9}{14} \\end{bmatrix}$	f	\N	\N
1077	319	$\\begin{bmatrix} \\frac{3}{14} \\\\ \\frac{6}{14} \\\\ -\\frac{9}{14} \\end{bmatrix}$	f	\N	\N
1211	358	$[-1, 1, -3]$	f	\N	\N
1212	358	$[-3, 0, 1]$	t	\N	\N
1213	359	1	t	\N	\N
1214	359	2	f	\N	\N
1215	359	3	f	\N	\N
1216	359	4	f	\N	\N
1217	360	The first quadrant	f	\N	\N
1218	360	The first and the third quadrant	f	\N	\N
1219	360	The first and second quadrant	f	\N	\N
1220	360	The whole space $\\mathbb{R}^2$	t	\N	\N
1221	361	Rank = 2	f	\N	\N
1222	361	Rank = 1	t	\N	\N
1223	361	Rank = 0	f	\N	\N
1224	361	Rank = 4	f	\N	\N
1225	362	$(3,4)$	f	\N	\N
1226	362	$(4,3)$	f	\N	\N
1227	362	$(5,3)$	t	\N	\N
1228	362	$(3,5)$	t	\N	\N
1229	363	$\\text{Span } \\left\\{ \\begin{bmatrix} -9 \\\\ 3 \\\\ 1 \\\\ 0 \\end{bmatrix}, \\begin{bmatrix} -2 \\\\ -1 \\\\ 0 \\\\ 1 \\end{bmatrix} \\right\\}$	t	\N	\N
1230	363	$\\text{Span } \\left\\{ \\begin{bmatrix} 9 \\\\ 3 \\\\ 1 \\\\ 0 \\end{bmatrix}, \\begin{bmatrix} -2 \\\\ 1 \\\\ 0 \\\\ 1 \\end{bmatrix} \\right\\}$	f	\N	\N
1231	363	$\\text{Span } \\left\\{ \\begin{bmatrix} 9 \\\\ 3 \\\\ 1 \\\\ 0 \\end{bmatrix}, \\begin{bmatrix} 2 \\\\ 1 \\\\ 0 \\\\ 1 \\end{bmatrix} \\right\\}$	f	\N	\N
1232	363	$\\text{Span } \\left\\{ \\begin{bmatrix} 1 \\\\ 3 \\\\ 1 \\\\ 0 \\end{bmatrix}, \\begin{bmatrix} 0 \\\\ -1 \\\\ 0 \\\\ 1 \\end{bmatrix} \\right\\}$	f	\N	\N
1233	364	$[1, 2, 3], [-1, -2, 3]$	f	\N	\N
1234	364	$[1, 2, 1], [0, -1, 2]$	t	\N	\N
1235	364	$[1, 2, 5], [1, 2, 3]$	f	\N	\N
1236	364	$[1, 2, 3], [2, 4, 6]$	f	\N	\N
1237	364	$[1, 2, 1], [-1, 0, -1]$	f	\N	\N
1238	365	$\\begin{bmatrix} \\frac{27}{29} \\\\ -\\frac{18}{29} \\\\ \\frac{36}{29} \\end{bmatrix}$	f	\N	\N
1239	365	$\\begin{bmatrix} \\frac{27}{29} \\\\ \\frac{18}{29} \\\\ \\frac{36}{29} \\end{bmatrix}$	f	\N	\N
1240	365	$\\begin{bmatrix} \\frac{81}{29} \\\\ -\\frac{54}{29} \\\\ \\frac{108}{29} \\end{bmatrix}$	t	\N	\N
1241	365	$\\begin{bmatrix} \\frac{81}{29} \\\\ \\frac{54}{29} \\\\ \\frac{108}{29} \\end{bmatrix}$	f	\N	\N
1242	366	$\\frac{1}{14} \\begin{bmatrix} 4 & 2 & 6 \\\\ 2 & 1 & 3 \\\\ 6 & 3 & 9 \\end{bmatrix}$	t	\N	\N
1243	366	$\\frac{1}{14} \\begin{bmatrix} 4 & 2 & 9 \\\\ 3 & 2 & 3 \\\\ 6 & 3 & 9 \\end{bmatrix}$	f	\N	\N
1244	366	$\\frac{1}{14} \\begin{bmatrix} 4 & 3 & 6 \\\\ -2 & 1 & 6 \\\\ 6 & 3 & 9 \\end{bmatrix}$	f	\N	\N
1245	366	$\\frac{1}{14} \\begin{bmatrix} 2 & 2 & 5 \\\\ 2 & -1 & 7 \\\\ -6 & 5 & 9 \\end{bmatrix}$	f	\N	\N
1246	367	$\\begin{bmatrix} -\\frac{32}{9} \\\\ -\\frac{32}{9} \\\\ \\frac{16}{9} \\end{bmatrix}$	f	\N	\N
1247	367	$\\begin{bmatrix} \\frac{32}{9} \\\\ -\\frac{32}{9} \\\\ \\frac{16}{9} \\end{bmatrix}$	t	\N	\N
1248	367	$\\begin{bmatrix} \\frac{32}{9} \\\\ \\frac{16}{9} \\\\ -\\frac{32}{9} \\end{bmatrix}$	f	\N	\N
1249	367	$\\begin{bmatrix} \\frac{32}{9} \\\\ -\\frac{16}{9} \\\\ \\frac{32}{9} \\end{bmatrix}$	f	\N	\N
1250	368	$\\mathbb{Z}$	f	\N	\N
1251	368	$(-5, 5)$	f	\N	\N
1252	368	$\\mathbb{R}^6$	f	\N	\N
1253	368	$\\mathbb{R}$	t	\N	\N
1254	369	$\\{(a,b) : a,b \\in \\mathbb{R}^d\\}$	f	\N	\N
1255	369	$\\{(x_1,x_2,...,x_d) : x_i \\in \\mathbb{R}, \\forall 1 < i \\leq d\\}$	f	\N	\N
1256	369	$\\{x \\in \\mathbb{R}^d : x_i \\in \\{a,b\\}, i \\in \\{1,2,...,d\\}\\}$	f	\N	\N
1257	369	$\\{x \\in \\mathbb{R}^d : x_i \\in [a,b], i \\in \\{1,2,...,d\\}\\}$	t	\N	\N
1258	370	their linear combination belongs to $V$.	t	\N	\N
1259	370	their linear combination is perpendicular to $V$.	f	\N	\N
1260	370	their linear combination is zero.	f	\N	\N
1261	370	their linear combination may belong to any vector space other than $V$.	f	\N	\N
1262	371	$(A \\cup B)^C = A^C \\cap B^C$	f	\N	\N
1263	371	$(A \\cap B)^C = A^C \\cup B^C$	f	\N	\N
1264	371	$(A^C \\cup B^C)^C = A \\cap B$	f	\N	\N
1265	371	$(A^C \\cap B^C)^C = A \\cup B$	f	\N	\N
1266	371	All of these.	t	\N	\N
1267	372	$x.y = 0$	t	\N	\N
1268	372	$x.y = 1$	f	\N	\N
1269	372	$x^Ty = 0$	t	\N	\N
1270	372	$x^Ty = 1$	f	\N	\N
1271	373	Domain is $\\mathbb{R}$	f	\N	\N
1272	373	Co-domain is $\\mathbb{R}$	t	\N	\N
1273	373	Both domain and co-domain are $\\mathbb{R}$	f	\N	\N
1274	374	it is continuous at atleast one point in $\\mathbb{R}$.	f	\N	\N
1275	374	it is continuous at atmost one point in $\\mathbb{R}$.	f	\N	\N
1973	558	negative semi-definite	f	\N	\N
635	61	Red, 100px, 100px	f	\N	\N
521	259	The two lines are always the same.	t	\N	\N
523	259	The two lines are the same if and only if word1 and word2 are equal.	f	\N	\N
1078	320	0	f	\N	\N
1079	320	1	t	\N	\N
1080	320	-1	f	\N	\N
1081	321	-1	f	\N	\N
1082	321	0	t	\N	\N
1083	321	1	f	\N	\N
1084	321	-2	f	\N	\N
1085	322	-1, 3	f	\N	\N
1086	322	1, 3	t	\N	\N
1087	322	1, -3	f	\N	\N
1088	322	0, 4	f	\N	\N
1089	325	$\\lambda^2-4\\lambda-1$	t	\N	\N
1090	325	$\\lambda^2-4\\lambda$	f	\N	\N
1091	325	$\\lambda^2-4\\lambda-3$	f	\N	\N
1092	325	$\\lambda^2+4\\lambda+3$	f	\N	\N
1093	325	$\\lambda^2-4\\lambda+3$	f	\N	\N
1094	326	$2+\\sqrt{5}, 2-\\sqrt{5}$	t	\N	\N
1095	326	$\\sqrt{5}, -\\sqrt{5}$	f	\N	\N
1096	326	0, 1	f	\N	\N
1097	326	$2+\\sqrt{3}, 2-\\sqrt{3}$	f	\N	\N
1098	326	$\\sqrt{3}, -\\sqrt{3}$	f	\N	\N
1099	327	-1, 2 and -3	f	\N	\N
1100	327	1, 4 and 9	t	\N	\N
1101	327	-1, -4 and -9	f	\N	\N
1102	327	1, -2 and 3	f	\N	\N
1103	328	$\\frac{1}{\\sqrt{5}} \\left( \\frac{1+\\sqrt{5}}{2} \\right)^{90}$	t	\N	\N
1104	328	$\\frac{1}{\\sqrt{5}} \\left( \\frac{1-\\sqrt{5}}{2} \\right)^{90}$	f	\N	\N
1105	328	$\\frac{1}{\\sqrt{5}} \\left( \\frac{1+\\sqrt{5}}{2} \\right)^{-90}$	f	\N	\N
1106	328	$-\\frac{1}{\\sqrt{5}} \\left( \\frac{1+\\sqrt{5}}{2} \\right)^{90}$	f	\N	\N
1107	329	1, 2, 3 and 4	f	\N	\N
1108	329	1, 2 and 3	f	\N	\N
1109	329	1, 2 and 4	t	\N	\N
1110	329	2, 3 and 4	f	\N	\N
1111	330	$A$ is orthogonally diagonalizable.	f	\N	\N
1112	330	Eigenvalues of $A$ are real.	f	\N	\N
1113	330	Eigenvectors corresponding to different eigenvalues are independent.	f	\N	\N
1114	330	All of these	t	\N	\N
1115	331	5	t	\N	\N
1116	331	-2	f	\N	\N
1117	331	-1	t	\N	\N
1118	331	3	f	\N	\N
1119	332	$\\begin{bmatrix} 1 \\\\ 2 \\end{bmatrix}$	f	\N	\N
1120	332	$\\begin{bmatrix} 2 \\\\ 3 \\end{bmatrix}$	t	\N	\N
1121	332	$\\begin{bmatrix} 1 \\\\ -1 \\end{bmatrix}$	t	\N	\N
1122	332	$\\begin{bmatrix} 1 \\\\ 1 \\end{bmatrix}$	f	\N	\N
1123	332	$\\begin{bmatrix} 2 \\\\ -3 \\end{bmatrix}$	f	\N	\N
1124	333	only 1	t	\N	\N
1125	333	only 2	f	\N	\N
1126	333	both 1 and 2	f	\N	\N
1127	333	neither 1 nor 2	f	\N	\N
1189	353	$P^T=P$	f	\N	\N
1190	353	$P^T=-P$	f	\N	\N
1191	353	$P^{-1}=P$	f	\N	\N
1192	353	$P^T=P^{-1}$	t	\N	\N
1128	334	$1.35x^2+0.3x$	f	\N	\N
1129	334	$1.25x^2+0.45x$	f	\N	\N
1130	334	$-0.3x^2+1.45x$	t	\N	\N
1131	334	$-0.25x^2+0.5$	f	\N	\N
1132	335	$L(\\theta)=\\frac{1}{2}(A\\theta-Y)(A\\theta-Y)^T$	f	\N	\N
1133	335	$L(\\theta)=\\frac{1}{2}(A\\theta-Y)^T(A\\theta-Y)$	t	\N	\N
1134	335	$L(\\theta)=\\frac{1}{2}(A\\theta-Y)^2$	f	\N	\N
1135	336	A has rank 1	f	\N	\N
1136	336	A is full rank	t	\N	\N
1137	336	A is singular	f	\N	\N
1138	336	A is a projection matrix	f	\N	\N
1139	337	True	t	\N	\N
1140	337	False	f	\N	\N
1141	338	True	t	\N	\N
1142	338	False	f	\N	\N
1143	339	the column space of $A$	f	\N	\N
1144	339	the null space of $A$	t	\N	\N
1145	339	the row space of $A$	f	\N	\N
1146	339	the left null space of $A$	f	\N	\N
1147	340	there may be imaginary eigenvalues	f	\N	\N
1148	340	the eigenvalues are always identical	f	\N	\N
1149	340	the eigenvalues are always real	t	\N	\N
1150	341	null space of $A$	f	\N	\N
1151	341	null space of $\\lambda I$	f	\N	\N
1152	341	null space of $A-\\lambda I$	t	\N	\N
1153	341	null space of $A\\lambda$	f	\N	\N
1154	342	Eigenvectors of $A$ are orthogonal to eigenvectors of $B$	f	\N	\N
1155	342	Eigenvectors of $A$ are orthonormal to eigenvectors of $B$	f	\N	\N
1156	342	Eigenvectors of $A$ are same as the eigenvectors of $B$	t	\N	\N
1157	343	an identity matrix	f	\N	\N
1158	343	a singular matrix	t	\N	\N
1159	343	a non singular matrix	f	\N	\N
1160	343	a zero matrix	f	\N	\N
1161	344	True	t	\N	\N
1162	344	False	f	\N	\N
1163	345	0	f	\N	\N
1164	345	1	f	\N	\N
1165	345	-1	f	\N	\N
1166	345	1 or -1	t	\N	\N
1167	346	True	f	\N	\N
1168	346	False	t	\N	\N
1169	347	True	t	\N	\N
1170	347	False	f	\N	\N
1175	349	True	f	\N	\N
1176	349	False	t	\N	\N
1171	348	Neither 1 nor 2	f	\N	\N
1172	348	1	f	\N	\N
1173	348	2	f	\N	\N
1174	348	1 and 2	t	\N	\N
1177	350	$S^{-1}A^kS=\\Lambda$	f	\N	\N
1178	350	$S^{-1}A^kS=\\Lambda^k$	t	\N	\N
1179	350	$S^{-1}A^kS=\\Lambda^{-1}$	f	\N	\N
1180	350	$SAS^{-1}=\\Lambda$	f	\N	\N
1181	351	$\\frac{1+\\sqrt{5}}{2}, \\frac{1-\\sqrt{5}}{2}$	t	\N	\N
1182	351	$\\frac{\\sqrt{5}}{2}, \\frac{-\\sqrt{5}}{2}$	f	\N	\N
1183	351	$\\frac{2+\\sqrt{5}}{2}, \\frac{2-\\sqrt{5}}{2}$	f	\N	\N
1184	351	$1, 0$	f	\N	\N
1185	352	$\\begin{bmatrix} \\frac{1+\\sqrt{5}}{2} \\\\ 1 \\end{bmatrix}, \\begin{bmatrix} \\frac{1-\\sqrt{5}}{2} \\\\ 1 \\end{bmatrix}$	t	\N	\N
1186	352	$\\begin{bmatrix} 1 \\\\ 1 \\end{bmatrix}, \\begin{bmatrix} \\frac{1-\\sqrt{5}}{2} \\\\ 1 \\end{bmatrix}$	f	\N	\N
1187	352	$\\begin{bmatrix} \\frac{1+\\sqrt{5}}{2} \\\\ 1 \\end{bmatrix}, \\begin{bmatrix} 1 \\\\ 1 \\end{bmatrix}$	f	\N	\N
1188	352	$\\begin{bmatrix} \\frac{-1+\\sqrt{5}}{2} \\\\ 1 \\end{bmatrix}, \\begin{bmatrix} \\frac{-1-\\sqrt{5}}{2} \\\\ 1 \\end{bmatrix}$	f	\N	\N
1193	354	1	f	\N	\N
1194	354	2	t	\N	\N
1195	354	3	t	\N	\N
1196	354	4	f	\N	\N
1197	355	2.342	f	\N	\N
1198	355	2.308	f	\N	\N
1199	355	2.440	f	\N	\N
1200	355	2.449	t	\N	\N
1201	356	11	f	\N	\N
1202	356	12	f	\N	\N
1203	356	14	f	\N	\N
1204	356	16	t	\N	\N
1205	357	3	f	\N	\N
1206	357	1	f	\N	\N
931	283	It consists of linear combinations of the column vectors of $A^T$.	f	\N	\N
932	283	It consists of linear combinations of the column vectors of $A$.	t	\N	\N
933	283	It is the span of the column vectors of $A$.	t	\N	\N
934	283	It is the span of the column vectors of $A^T$.	f	\N	\N
935	284	True	t	\N	\N
936	284	False	f	\N	\N
937	285	It is those $b$ for which $Ax=b$ has a solution.	f	\N	\N
938	285	It is those $x$ that satisfy $A^Tx=0$.	f	\N	\N
939	285	It is those $x$ that satisfy $Ax=0$.	t	\N	\N
940	285	It is those $b$ for which $A^Tx=b$ has a solution.	f	\N	\N
941	286	$Ax=0$	t	\N	\N
942	286	$Ax \\neq 0$	f	\N	\N
943	286	$Ax=b$, for some $b \\in C(A)$	f	\N	\N
944	286	$Ax=b$, for some $b \\in R(A)$	f	\N	\N
945	287	True	f	\N	\N
946	287	False	t	\N	\N
947	288	$C(A)$ is $\\mathbb{R}^n$	f	\N	\N
948	288	$Ax=b$ has infinite solutions.	t	\N	\N
949	288	$Ax=b$ has a unique solution.	f	\N	\N
950	288	$N(A)$ only contain zero vector.	f	\N	\N
951	289	$\\text{dim}(C(A)) + \\text{dim}(N(A)) = n$	t	\N	\N
952	289	$\\text{dim}(C(A)) + \\text{dim}(N(A)) = m$	f	\N	\N
953	289	$\\text{rank}(A) + \\text{nullity}(A) = m$	f	\N	\N
954	289	$\\text{rank}(A) + \\text{nullity}(A) = n$	t	\N	\N
955	289	$\\text{dim}(C(A^T)) + \\text{dim}(N(A^T)) = m$	t	\N	\N
956	289	$\\text{dim}(C(A^T)) + \\text{dim}(N(A^T)) = n$	f	\N	\N
957	290	1 and 2	t	\N	\N
958	290	1 and 3	f	\N	\N
959	290	2 and 3	f	\N	\N
960	290	3 and 4	f	\N	\N
961	291	$xx^T$	f	\N	\N
962	291	$x^Tx$	f	\N	\N
963	291	$\\sqrt{xx^T}$	f	\N	\N
964	291	$\\sqrt{x^Tx}$	t	\N	\N
965	292	$x^Ty=1$	f	\N	\N
966	292	$x^Ty=0$	t	\N	\N
967	292	$y^Tx=0$	t	\N	\N
968	292	$y^Tx=1$	f	\N	\N
969	292	$x.y=1$	f	\N	\N
970	292	$x.y=0$	t	\N	\N
971	292	$y.x=1$	f	\N	\N
972	292	$y.x=0$	t	\N	\N
973	293	Unit vector	f	\N	\N
974	293	Zero vector	t	\N	\N
975	293	None of the above	f	\N	\N
976	294	True	f	\N	\N
977	294	False	t	\N	\N
978	295	$x.y=0$ and $||x||=||y||=0$	f	\N	\N
979	295	$x.y=0$ and $||x||=||y||=1$	t	\N	\N
980	295	$x.y=1$ and $||x||=||y||=0$	f	\N	\N
981	295	$x.y=1$ and $||x||=||y||=1$	f	\N	\N
982	296	$x^Ty=0, \\forall x \\in S_1, \\forall y \\in S_2$	t	\N	\N
983	296	$x^Ty=1, \\forall x \\in S_1, \\forall y \\in S_2$	f	\N	\N
984	296	$x^Ty=0, \\exists x \\in S_1, \\forall y \\in S_2$	f	\N	\N
985	296	$x^Ty=1, \\exists x \\in S_1, \\forall y \\in S_2$	f	\N	\N
986	296	$x^Ty=0, \\forall x \\in S_1, \\exists y \\in S_2$	f	\N	\N
987	296	$x^Ty=1, \\forall x \\in S_1, \\exists y \\in S_2$	f	\N	\N
988	296	$x^Ty=0, \\exists x \\in S_1, \\exists y \\in S_2$	f	\N	\N
989	296	$x^Ty=1, \\exists x \\in S_1, \\exists y \\in S_2$	f	\N	\N
990	297	$C(A) \\perp N(A)$	f	\N	\N
991	297	$R(A) \\perp N(A)$	t	\N	\N
992	297	$C(A) \\perp N(A^T)$	t	\N	\N
993	297	$R(A) \\perp N(A^T)$	f	\N	\N
994	298	$b \\in R(A)$	f	\N	\N
995	298	$b \\notin R(A)$	f	\N	\N
996	298	$b \\in C(A)$	f	\N	\N
997	298	$b \\notin C(A)$	t	\N	\N
998	299	a line parallel to the line through $v$.	f	\N	\N
999	299	a line passing through $v$.	t	\N	\N
1000	299	a line perpendicular to the line through $v$.	f	\N	\N
1001	300	1 only	f	\N	\N
1002	300	1 and 2	t	\N	\N
1003	300	2 only	f	\N	\N
1004	300	1, 2 and 3	f	\N	\N
1005	300	3 and 4	f	\N	\N
1006	301	a line parallel to the line through $v$.	f	\N	\N
1007	301	a line passing through $v$.	f	\N	\N
1008	301	a line perpendicular to the line through $v$.	f	\N	\N
1009	301	a plane orthogonal to $v$.	t	\N	\N
1010	302	$\\frac{||a||^2}{aa^T}$	f	\N	\N
1011	302	$\\frac{a^Ta}{aa^T}$	f	\N	\N
1012	302	$\\frac{aa^T}{a^Ta}$	t	\N	\N
1013	302	$\\frac{aa^T}{||a||^2}$	t	\N	\N
1014	303	$C(A)=\\mathbb{R}^n$	f	\N	\N
1015	303	$R(A)=\\mathbb{R}^n$	f	\N	\N
1016	303	$\\text{Rank}(A) = n$	f	\N	\N
1017	303	All of these	t	\N	\N
1018	304	$b \\in C(A)$	t	\N	\N
1019	304	$b \\in R(A)$	f	\N	\N
1020	304	$b \\in N(A)$	f	\N	\N
1021	304	$b \\in N(A^T)$	f	\N	\N
1022	305	1 and 3	t	\N	\N
1023	305	2 and 3	f	\N	\N
1024	305	2 and 4	f	\N	\N
1025	305	1 and 4	f	\N	\N
1026	306	$||A\\theta-b||^2=1$	f	\N	\N
1027	306	$||A\\theta-b||^2=0$	t	\N	\N
1028	306	$||A\\theta-b||^2>0$	f	\N	\N
1029	306	$||A\\theta-b||^2<0$	f	\N	\N
1030	307	aims to minimize $||A\\theta-b||$	t	\N	\N
1031	307	aims to maximize $||A\\theta-b||$	f	\N	\N
1032	308	projects $b$ onto $R(A)$	f	\N	\N
1033	308	projects $b$ onto $C(A)$	t	\N	\N
1034	308	projects $b$ onto $N(A)$	f	\N	\N
1035	308	projects $b$ onto $N(A^T)$	f	\N	\N
1036	309	1.73	t	\N	\N
1037	309	1.71	f	\N	\N
1038	309	1.72	f	\N	\N
1039	309	1.74	f	\N	\N
1040	310	11	t	\N	\N
1041	310	12	f	\N	\N
1042	310	31	f	\N	\N
1043	310	20	f	\N	\N
1044	311	0	f	\N	\N
1045	311	1	f	\N	\N
1046	311	2	t	\N	\N
1047	311	3	f	\N	\N
1048	312	0	f	\N	\N
1049	312	1	f	\N	\N
1050	312	2	f	\N	\N
1051	312	3	t	\N	\N
1052	313	Yes	t	\N	\N
1053	313	No	f	\N	\N
1054	314	0	f	\N	\N
1055	314	1	f	\N	\N
1056	314	2	t	\N	\N
1057	314	3	f	\N	\N
1058	315	1	f	\N	\N
1059	315	2	f	\N	\N
1060	315	3	t	\N	\N
1061	315	4	f	\N	\N
1062	316	3	f	\N	\N
1063	316	1	t	\N	\N
1064	316	2	f	\N	\N
1065	316	4	f	\N	\N
1207	357	2	t	\N	\N
1208	357	4	f	\N	\N
1276	374	it is continuous at all points in $\\mathbb{R}$.	t	\N	\N
1277	375	True	t	\N	\N
1278	375	False	f	\N	\N
1279	376	If a function is continuous at a point, then it is also differentiable at that point.	f	\N	\N
1280	376	If a function is differentiable at a point, then it is also continuous at that point.	t	\N	\N
1281	376	If a function is not continuous at a point, then it is not differentiable at that point.	t	\N	\N
1282	376	If a function is not differentiable at a point, then it may or may not be continuous at that point.	t	\N	\N
1283	377	for any sequence of $x_i$ converging to $x_0$, $f(x_i)$ converges to $x_0$.	f	\N	\N
1284	377	for any sequence of $x_i$ converging to $x_0$, $f(x_i)$ converges to $f(x_0)$.	t	\N	\N
1285	377	for any sequence of $x_i$ converging to $x_0$, $f(x_i)$ converge to zero.	f	\N	\N
1286	378	True	t	\N	\N
1287	378	False	f	\N	\N
1288	379	perpendicular to $f$.	f	\N	\N
1289	379	parallel to $f$	f	\N	\N
1290	379	tangent to $f$ at the point $(v,f(v))$.	t	\N	\N
1291	381	$[1, 1, 1]$	f	\N	\N
1292	381	$[0, 1, 1]$	f	\N	\N
1293	381	$[1, 0, 1]$	f	\N	\N
1294	381	$[0, 0, 0]$	t	\N	\N
1295	381	$[-1, 0, 1]$	f	\N	\N
1296	382	$f:\\mathbb{R} \\rightarrow \\mathbb{R}$	f	\N	\N
1297	382	$f:\\mathbb{R}^d \\rightarrow \\mathbb{R}$	t	\N	\N
1298	382	$f:\\mathbb{R} \\rightarrow \\mathbb{R}^d$	f	\N	\N
1299	382	$f:\\mathbb{R} \\rightarrow \\mathbb{R} \\times \\mathbb{R}$	f	\N	\N
1300	383	True	t	\N	\N
1301	383	False	f	\N	\N
1302	384	0	f	\N	\N
1303	384	0.5	t	\N	\N
1304	384	1	f	\N	\N
1305	384	-1	f	\N	\N
1306	385	the critical point represents maxima.	f	\N	\N
1307	385	the critical point represents minima.	t	\N	\N
1308	385	the critical point is a saddle point.	f	\N	\N
1309	386	True	t	\N	\N
1310	386	False	f	\N	\N
1311	387	True	t	\N	\N
1312	387	False	f	\N	\N
1313	388	equidistantly spaced circles.	f	\N	\N
1314	388	non-uniformly spaced circles.	f	\N	\N
1315	388	equidistantly spaced straight lines.	t	\N	\N
1316	388	non-uniformly spaced straight lines.	f	\N	\N
1317	389	$\\{x : x = \\begin{bmatrix} 1 \\\\ -1 \\end{bmatrix} + \\alpha \\begin{bmatrix} 1 \\\\ 3 \\end{bmatrix}, \\alpha \\in \\mathbb{R}\\}$	t	\N	\N
1318	389	$\\{x : x = \\begin{bmatrix} -1 \\\\ -1 \\end{bmatrix} + \\alpha \\begin{bmatrix} 1 \\\\ 3 \\end{bmatrix}, \\alpha \\in \\mathbb{R}\\}$	f	\N	\N
1319	389	$\\{x : x = \\begin{bmatrix} -1 \\\\ 1 \\end{bmatrix} + \\alpha \\begin{bmatrix} 1 \\\\ 3 \\end{bmatrix}, \\alpha \\in \\mathbb{R}\\}$	f	\N	\N
1320	389	$\\{x : x = \\begin{bmatrix} 1 \\\\ -1 \\end{bmatrix} + \\alpha \\begin{bmatrix} 1 \\\\ -3 \\end{bmatrix}, \\alpha \\in \\mathbb{R}\\}$	f	\N	\N
1321	390	True	f	\N	\N
1322	390	False	t	\N	\N
1323	391	$\\bar{x}_1^Tx_1, \\bar{x}_2^Tx_2$	t	\N	\N
1324	391	$x_1^Tx_1, x_2^Tx_2$	f	\N	\N
1325	391	$\\bar{x}_1^Tx_1, x_2^Tx_2$	f	\N	\N
1326	391	$x_1^Tx_1, \\bar{x}_2^Tx_2$	t	\N	\N
1327	392	transpose of $A$	f	\N	\N
1328	392	transpose of conjugate of $A$	t	\N	\N
1329	392	conjugate of transpose of $A$	t	\N	\N
1330	392	conjugate of $A$	f	\N	\N
1331	393	$(A^*)^* = A^*$	f	\N	\N
1332	393	$(A^*)^* = A$	t	\N	\N
1333	393	$(AB)^* = A^*B^*$	f	\N	\N
1334	393	$(AB)^* = B^*A^*$	t	\N	\N
1335	394	1 and 3	f	\N	\N
1336	394	1, 3 and 4	f	\N	\N
1337	394	2, 3 and 4	t	\N	\N
1338	394	2 and 3	f	\N	\N
1339	395	$\\begin{bmatrix} 1 & 1-i \\\\ 2+3i & 2i \\end{bmatrix}$	f	\N	\N
1340	395	$\\begin{bmatrix} 1 & 2-3i \\\\ 1+i & 2i \\end{bmatrix}$	f	\N	\N
1341	395	$\\begin{bmatrix} 1 & 1-i \\\\ 2-3i & 2i \\end{bmatrix}$	f	\N	\N
1342	395	$\\begin{bmatrix} 1 & 2+3i \\\\ 1+i & -2i \\end{bmatrix}$	t	\N	\N
1343	396	diagonal matrices in a real vector space	f	\N	\N
1344	396	identity matrices in a real vector space	f	\N	\N
1345	396	symmetric matrices in a real vector space	t	\N	\N
1346	396	orthogonal matrices in a real vector space	f	\N	\N
1347	397	True	t	\N	\N
1348	397	False	f	\N	\N
1349	398	true for all Hermitian matrices	t	\N	\N
1350	398	true for some Hermitian matrices	f	\N	\N
1351	398	false for all Hermitian matrices	f	\N	\N
1352	399	always real	t	\N	\N
1353	399	always irrational	f	\N	\N
1354	399	always rational	f	\N	\N
1355	399	always complex	f	\N	\N
1356	400	True	t	\N	\N
1357	400	False	f	\N	\N
1358	401	True	t	\N	\N
1359	401	False	f	\N	\N
1360	402	it is a square matrix and has orthogonal columns	t	\N	\N
1361	402	it is a square matrix and has orthonormal columns	t	\N	\N
1362	402	$U^*=U$	f	\N	\N
1363	402	$U^*=U^{-1}$	f	\N	\N
1364	403	$U^*$ is unitary.	f	\N	\N
1365	403	$UU^*=I$	f	\N	\N
1366	403	The columns of $U$ form an orthonormal set.	f	\N	\N
1367	403	All of these.	t	\N	\N
1368	404	orthonormal	f	\N	\N
1369	404	orthogonal	t	\N	\N
1370	404	of unit length	f	\N	\N
1371	405	True	f	\N	\N
1372	405	False	t	\N	\N
1373	406	$\\lambda=1$	f	\N	\N
1374	406	$|\\lambda|=1$	t	\N	\N
1375	406	$\\lambda=0$	f	\N	\N
1376	406	$|\\lambda| \\geq 1$	f	\N	\N
1377	407	unitary, unitary	f	\N	\N
1378	407	Hermitian, Hermitian	f	\N	\N
1379	407	unitary, Hermitian	f	\N	\N
1380	407	Hermitian, unitary	t	\N	\N
1381	408	Any $n \\times n$ matrix $A$ is unitarily diagonalizable.	f	\N	\N
1382	408	Any $m \\times n$ matrix $A$ is unitarily diagonalizable.	f	\N	\N
1383	408	Any Hermitian matrix $A$ is unitarily diagonalizable.	t	\N	\N
1384	408	Any upper triangular matrix $A$ is unitarily diagonalizable.	f	\N	\N
1385	409	Given a Hermitian matrix $A$, there exists a unitary matrix $U$ and a diagonal matrix $D$ such that $D=U^*AU$.	f	\N	\N
1386	409	Given a Hermitian matrix $A$, there exists a unitary matrix $U$ and a diagonal matrix $D$ such that $A=U^*DU$.	f	\N	\N
1387	409	Given an $n \\times n$ matrix $A$, there exists a unitary matrix $U$ and an upper triangular matrix $T$ such that $A=UTU^*$.	t	\N	\N
1388	409	Given an $n \\times n$ matrix $A$, there exists a unitary matrix $U$ and an upper triangular matrix $T$ such that $T=UAU^*$.	f	\N	\N
1389	410	an upper triangular matrix.	f	\N	\N
1390	410	a lower triangular matrix.	f	\N	\N
1391	410	a diagonal matrix with complex entries.	f	\N	\N
1392	410	a diagonal matrix with real entries.	t	\N	\N
1393	411	True	f	\N	\N
1394	411	False	t	\N	\N
1395	412	True	t	\N	\N
1396	412	False	f	\N	\N
1397	413	$\\begin{bmatrix} 1-i & 6+4i \\\\ 1-3i & 35-2i \\end{bmatrix}$	f	\N	\N
1398	413	$\\begin{bmatrix} 1+i & 6-4i \\\\ 1+3i & 35+2i \\end{bmatrix}$	t	\N	\N
1399	413	$\\begin{bmatrix} -1+i & -6+4i \\\\ -1-3i & -35-2i \\end{bmatrix}$	f	\N	\N
1400	413	$\\begin{bmatrix} 1-i & 6-4i \\\\ 1-3i & 35-2i \\end{bmatrix}$	f	\N	\N
1401	414	$\\begin{bmatrix} -3+2i & 5-i \\\\ 1-4i & -7+2i \\end{bmatrix}$	f	\N	\N
1402	414	$\\begin{bmatrix} 3+2i & 1-4i \\\\ 5-i & 7+2i \\end{bmatrix}$	f	\N	\N
1403	414	$\\begin{bmatrix} 3+2i & 1-4i \\\\ 5-i & 7-2i \\end{bmatrix}$	f	\N	\N
1404	414	$\\begin{bmatrix} 3+2i & 5-i \\\\ 1-4i & 7+2i \\end{bmatrix}$	t	\N	\N
1405	415	7-6i	f	\N	\N
1406	415	4-4i	f	\N	\N
1407	415	2-2i	t	\N	\N
1408	415	3+4i	f	\N	\N
1409	416	4.69	f	\N	\N
1410	416	20	f	\N	\N
1411	416	4.47	f	\N	\N
1412	416	22	t	\N	\N
1413	417	True	f	\N	\N
1414	417	False	t	\N	\N
1415	418	True	t	\N	\N
1416	418	False	f	\N	\N
1417	419	$\\begin{bmatrix} 1 & 3+i \\\\ 3-i & i \\end{bmatrix}$	f	\N	\N
1418	419	$\\begin{bmatrix} 0 & 3-2i \\\\ 3-2i & 4 \\end{bmatrix}$	f	\N	\N
1419	419	$\\begin{bmatrix} 3 & 2+i & 3i \\\\ 2-i & 0 & 1+i \\\\ -3i & 1-i & 0 \\end{bmatrix}$	t	\N	\N
1420	419	$\\begin{bmatrix} -1 & 2 & 3 \\\\ 2 & 0 & -1 \\\\ 3 & -1 & 4 \\end{bmatrix}$	t	\N	\N
1421	420	-1, -6 and 2	f	\N	\N
1422	420	1, -6 and -2	f	\N	\N
1423	420	1, 6 and 2	f	\N	\N
1424	420	-1, 6 and -2	t	\N	\N
1425	421	$\\frac{1}{2}$	t	\N	\N
1426	421	1	f	\N	\N
1427	421	$\\frac{1}{4}$	f	\N	\N
1428	421	$\\frac{1}{8}$	f	\N	\N
1429	422	$\\frac{1}{2}$	f	\N	\N
1430	422	1	f	\N	\N
1431	422	2	t	\N	\N
1432	422	$\\frac{1}{4}$	f	\N	\N
1433	423	$U=\\begin{bmatrix} \\frac{-1-i}{\\sqrt{3}} & \\frac{1}{\\sqrt{6}} \\\\ \\frac{1}{\\sqrt{3}} & \\frac{2}{\\sqrt{6}} \\end{bmatrix}, D=\\begin{bmatrix} 1 & 0 \\\\ 0 & 4 \\end{bmatrix}$	t	\N	\N
1434	423	$U=\\begin{bmatrix} \\frac{-1+i}{\\sqrt{3}} & \\frac{1}{\\sqrt{6}} \\\\ \\frac{1}{\\sqrt{3}} & \\frac{2}{\\sqrt{6}} \\end{bmatrix}, D=\\begin{bmatrix} 1 & 0 \\\\ 0 & 4 \\end{bmatrix}$	f	\N	\N
1435	423	$U=\\begin{bmatrix} \\frac{-1+i}{\\sqrt{3}} & \\frac{-1}{\\sqrt{6}} \\\\ \\frac{1}{\\sqrt{3}} & \\frac{-2}{\\sqrt{6}} \\end{bmatrix}, D=\\begin{bmatrix} 1 & 0 \\\\ 0 & 4 \\end{bmatrix}$	f	\N	\N
1436	423	$U=\\begin{bmatrix} \\frac{-1+i}{\\sqrt{3}} & \\frac{-1}{\\sqrt{6}} \\\\ \\frac{1}{\\sqrt{3}} & \\frac{-2}{\\sqrt{6}} \\end{bmatrix}, D=\\begin{bmatrix} -1 & 0 \\\\ 0 & -4 \\end{bmatrix}$	f	\N	\N
1437	424	$\\begin{bmatrix} \\frac{1}{\\sqrt{2}} & \\frac{i}{\\sqrt{2}} \\\\ \\frac{-i}{\\sqrt{2}} & \\frac{1}{\\sqrt{2}} \\end{bmatrix}$	f	\N	\N
1438	424	$\\begin{bmatrix} \\frac{-1}{\\sqrt{2}} & \\frac{i}{\\sqrt{2}} \\\\ \\frac{i}{\\sqrt{2}} & \\frac{1}{\\sqrt{2}} \\end{bmatrix}$	f	\N	\N
1439	424	$\\begin{bmatrix} \\frac{1}{\\sqrt{2}} & \\frac{i}{\\sqrt{2}} \\\\ \\frac{-i}{\\sqrt{2}} & \\frac{1}{\\sqrt{2}} \\end{bmatrix}$	f	\N	\N
1440	424	$\\begin{bmatrix} \\frac{1}{\\sqrt{2}} & \\frac{i}{\\sqrt{2}} \\\\ \\frac{i}{\\sqrt{2}} & \\frac{-1}{\\sqrt{2}} \\end{bmatrix}$	f	\N	\N
1441	424	$\\begin{bmatrix} \\frac{1}{\\sqrt{2}} & \\frac{i}{\\sqrt{2}} \\\\ \\frac{i}{\\sqrt{2}} & \\frac{1}{\\sqrt{2}} \\end{bmatrix}$	t	\N	\N
1442	425	both statements are true.	f	\N	\N
1443	425	both statements are false.	f	\N	\N
1444	425	1. is false.	t	\N	\N
1445	425	2. is false.	f	\N	\N
1450	427	v-bind directive is used for one way data binding.	t	\N	\N
1451	427	v-model directive is used for one way data binding.	f	\N	\N
1452	427	v-bind directive is used for two-way data binding.	f	\N	\N
1453	427	v-model directive is used for two-way data binding.	t	\N	\N
1467	431	undefined, 20	f	\N	\N
1460	429	20	f	\N	\N
1448	426	\N	f	code	addItem() {\r\n     this.items = 'New item'\r\n},
1449	426	All of the above	f	\N	\N
1454	428	total payable amount is 6000	f	\N	\N
1461	429	None of the above	f	\N	\N
1462	430	undefined, 40	t	\N	\N
1463	430	undefined, 20	f	\N	\N
1447	426	\N	t	code	addItem() {\r\n    this.items.push('New item')\r\n},
1468	431	20, 40	t	\N	\N
1469	431	40, 40	f	\N	\N
1470	432	v-if="player.team=='MI'" v-for="player in players", {{player.name}}	t	\N	\N
1464	430	20, 40	f	\N	\N
1465	430	40, 40	f	\N	\N
1466	431	undefined, 40	f	\N	\N
1458	429	0	f	\N	\N
1487	436	Welcome to iitm online degree	t	\N	\N
1489	436	None of the above	f	\N	\N
1490	437	v-bind="text"	f	\N	\N
1491	437	v-html="text"	t	\N	\N
1492	437	Both A and B	f	\N	\N
1493	437	None of the above	f	\N	\N
1446	426	\N	f	code	addItem() {\r\n     items.push('New item')\r\n},
1486	436	Welcome	f	\N	\N
1455	428	total payable amount is 8200	t	\N	\N
1456	428	total payable amount is 1800	f	\N	\N
1457	428	total payable amount is 7800	f	\N	\N
1459	429	1	t	\N	\N
1471	432	v-for="player in players" v-if="player.team=='MI'", {{players.name}}	f	\N	\N
1472	432	v-for="player in players" v-if="player.team=='MI'", {{player.name}}	t	\N	\N
1473	432	v-if="player.team=='MI'" v-for="player in players", {{players.name}}	f	\N	\N
1474	433	This is	f	\N	\N
1475	433	This is component 1	t	\N	\N
1476	433	No text will be shown	f	\N	\N
1477	433	None of the above	f	\N	\N
1478	434	This is	t	\N	\N
1479	434	This is component 1	f	\N	\N
1480	434	No text will be shown	f	\N	\N
1481	434	None of the above	f	\N	\N
1482	435	Hello:	f	\N	\N
1483	435	Hello: Welcome to IITM	t	\N	\N
1484	435	No text will be shown on the browser	f	\N	\N
1485	435	None of the above	f	\N	\N
1698	489	[1, 1, 1, 1, 1]	t	\N	\N
1498	439	It is a function which is triggered when the data it refers to changes.	t	\N	\N
1499	439	It is calculated each time it is used.	f	\N	\N
1500	439	It is generally used when some property is used at multiple places in an application.	t	\N	\N
1501	439	None of the above	f	\N	\N
1502	440	It is a function which is triggered when the property it refers to changes.	f	\N	\N
1503	440	Watchers are defined inside the watch object.	f	\N	\N
1504	440	Both A and B are correct.	t	\N	\N
1505	440	None of the above	f	\N	\N
1514	443	Vue framework can be used for creating Single Page Applications.	t	\N	\N
1515	443	VueJS can only be used in backend development.	f	\N	\N
1516	443	A Vue application cannot be integrated with an API.	f	\N	\N
1517	443	None of the above	f	\N	\N
1526	446	The message is: Abhishek	f	\N	\N
1527	446	The message is: Kumar	t	\N	\N
1528	446	The message is: Rajput	f	\N	\N
1529	446	The message is:	f	\N	\N
1699	489	[0, 0, 0, 0, 0]	f	\N	\N
1700	489	[1, 0, 1, 0, 1]	f	\N	\N
1701	489	[0, 1, 0, 1, 0]	f	\N	\N
1702	490	1	f	\N	\N
1488	436	App will give a warning and will show a blank page.	f	\N	\N
1494	438	toggleTheme() {\r\n       this.dark = !this.dark\r\n}	t	\N	\N
1495	438	toggleTheme() {\r\n      this.dark == !this.dark\r\n}	f	\N	\N
1496	438	toggleTheme() {\r\n     dark = !dark\r\n}	f	\N	\N
1497	438	toggleTheme() {\r\n      this.dark = divStyle\r\n}	f	\N	\N
1703	490	2	t	\N	\N
1704	490	3	f	\N	\N
1705	490	Undefined	f	\N	\N
1706	491	1	f	\N	\N
1506	441	This is	f	\N	\N
1507	441	This is component 1	f	\N	\N
1508	441	No text will be shown on the browser.	t	\N	\N
1509	441	None of the above	f	\N	\N
1707	491	2	f	\N	\N
1708	491	3	f	\N	\N
1709	491	Reference Error	t	\N	\N
1710	492	[2, 3]	t	\N	\N
1711	492	[1, 2, 3]	f	\N	\N
1712	492	[1]	f	\N	\N
1713	492	Reference Error	f	\N	\N
1714	493	5	f	\N	\N
1715	493	2	t	\N	\N
1716	493	3	f	\N	\N
1717	493	None of the above	f	\N	\N
1718	494	['0', '1', '2', '3', '4']	t	\N	\N
1719	494	[0, 1, 2, 3, 4]	f	\N	\N
1720	494	['1', '2', '3', '4', '5']	f	\N	\N
1721	494	[1, 2, 3, 4, 5]	f	\N	\N
1722	495	['0', '1', '2', '3', '4']	f	\N	\N
1723	495	[0, 1, 2, 3, 4]	f	\N	\N
1724	495	['1', '2', '3', '4', '5']	f	\N	\N
1725	495	[1, 2, 3, 4, 5]	t	\N	\N
1726	496	[[0, 1], [1, 2], [2, 3]]	f	\N	\N
1727	496	[['0', 1], ['1', 2], ['2', 3]]	t	\N	\N
1728	496	[[1, 1], [2, 2], [3, 3]]	f	\N	\N
1729	496	[['1', 1], ['2', 2], ['3', 3]]	f	\N	\N
1730	497	5	f	\N	\N
1510	442	\N	t	code	1.This is message1\n2.This is message2\n3.This is message3
1511	442	\N	f	code	1.This is message1\n1.This is message2\n1.This is message3
1512	442	\N	f	code	1.'This is message1'\n2.'This is message2'\n3.'This is message3'
1513	442	\N	f	code	1.'This is message1'\n1.'This is message2'\n1.'This is message3'
1518	444	VueJS is a JavaScript based reactive framework.	f	\N	\N
1519	444	VueJS is always rendered on the client side.	t	\N	\N
1520	444	VueJS requires the page to be refreshed to experience reactivity.	t	\N	\N
1521	444	All of the above	f	\N	\N
1522	445	“@click” can be used as a shorthand for v-on:click in event binding.	f	\N	\N
1523	445	Both v-if and v-show are used for conditional rendering.	f	\N	\N
1524	445	The Vue directive v-for is reactive.	f	\N	\N
1525	445	All of the above	t	\N	\N
1530	447	Computed property is generally derived from reactive properties of Vue instances.	t	\N	\N
1531	447	Computed properties are reactive.	t	\N	\N
1532	447	Computed properties are not reactive.	f	\N	\N
1533	447	None of the above	f	\N	\N
1534	448	Computed properties are by default getter only.	t	\N	\N
1535	448	A Computed property should be directly mutated.	f	\N	\N
1731	497	4	f	\N	\N
1732	497	9	t	\N	\N
1733	497	10	f	\N	\N
1734	498	9	f	\N	\N
1735	498	5	f	\N	\N
1736	498	3	f	\N	\N
1737	498	4	t	\N	\N
1738	499	[1, 2, ...a, 5]	f	\N	\N
1739	499	[1, 2, 2, 3, 4, 5]	t	\N	\N
1740	499	[1, 2, [2, 3, 4], 5]	f	\N	\N
1741	499	Error	f	\N	\N
1742	500	All the elements should be of the same datatype.	f	\N	\N
1743	500	It can contain elements of different datatypes.	t	\N	\N
1744	500	It is a collection.	t	\N	\N
1745	500	It cannot have more than one element.	f	\N	\N
1746	501	An Iterable is an object whose elements can be accessed sequentially.	t	\N	\N
1747	501	An iterator is an object whose elements can be accessed sequentially.	f	\N	\N
1748	501	An Iterable is an object that contains the pointer to the next element.	f	\N	\N
1749	501	An iterator is an object that contains the pointer to the next element.	t	\N	\N
1750	502	A function that is passed as an argument to a function.	t	\N	\N
1751	502	A function that can take function as an argument.	f	\N	\N
1752	502	Both	f	\N	\N
1753	502	None of the above	f	\N	\N
1754	503	String	t	\N	\N
1755	503	Array	t	\N	\N
1756	503	Set	t	\N	\N
1757	503	Number	f	\N	\N
1758	504	String	t	\N	\N
1759	504	Array	f	\N	\N
1760	504	Map	f	\N	\N
1761	504	Set	f	\N	\N
1974	559	(2, 1)	f	\N	\N
1975	559	(1, 2)	f	\N	\N
1976	559	(-1, 2)	f	\N	\N
1977	559	(2, -1)	t	\N	\N
1978	560	$\\begin{bmatrix} x & y & z \\end{bmatrix} \\begin{bmatrix} 1 & 0 & 1 \\\\ -1 & 1 & 1 \\\\ 0 & 0 & -1 \\end{bmatrix} \\begin{bmatrix} x \\\\ y \\\\ z \\end{bmatrix}$	t	\N	\N
1979	560	$\\begin{bmatrix} x & y & z \\end{bmatrix} \\begin{bmatrix} 1 & 0 & 1 \\\\ -1 & -1 & 1 \\\\ 0 & 0 & -1 \\end{bmatrix} \\begin{bmatrix} x \\\\ y \\\\ z \\end{bmatrix}$	f	\N	\N
1536	448	A Computed property should not be directly mutated.	t	\N	\N
1537	448	None of the above	f	\N	\N
1538	449	Computed properties are cached based on their reactive dependencies.	t	\N	\N
1539	449	Methods are cached based on their reactive dependencies.	f	\N	\N
1540	449	Computed properties are not cached based on their reactive dependencies.	f	\N	\N
1541	449	All of the above	f	\N	\N
1542	450	<div class="class1 class2">	t	\N	\N
1543	450	<div class="class2">	f	\N	\N
1544	450	<div class="class1">	f	\N	\N
1545	450	None of the above	f	\N	\N
1558	454	An element with v-if directive is always rendered irrespective of the condition’s truth value.	f	\N	\N
1559	454	An element with v-show directive is always rendered irrespective of the condition’s truth value.	t	\N	\N
1560	454	Both A and B	f	\N	\N
1561	454	None of the above	f	\N	\N
1562	455	v-if is evaluated first.	f	\N	\N
1563	455	v-for is evaluated first.	t	\N	\N
1564	455	Depends on the order.	f	\N	\N
1565	455	None of the above	f	\N	\N
1566	456	It allows us to directly reference the DOM element.	t	\N	\N
1567	456	Ref can be accessed only after the element is mounted.	t	\N	\N
1568	456	Ref can be accessed even before the element is mounted.	f	\N	\N
1569	456	None of the above	f	\N	\N
1546	451	<div class="class1 class2">	f	\N	\N
1547	451	<div class="class2">	f	\N	\N
1548	451	<div class="class1">	t	\N	\N
1549	451	None of the above	f	\N	\N
1550	452	Red, Normal	f	\N	\N
1551	452	Black, Normal	f	\N	\N
1552	452	Red, Bold	t	\N	\N
1553	452	Black, Bold	f	\N	\N
1554	453	Red, Bold	f	\N	\N
1555	453	Black, Normal	f	\N	\N
1556	453	Red, Normal	t	\N	\N
1557	453	Black, Bold	f	\N	\N
1570	457	User database of NPTEL	t	\N	\N
1571	457	List of emails selected for archiving in Gmail	f	\N	\N
1572	457	Google search index	t	\N	\N
1573	457	User shopping cart content on Amazon.in	f	\N	\N
1574	458	User database of NPTEL	f	\N	\N
1575	458	List of emails selected for archiving in Gmail	f	\N	\N
1576	458	Google search index	f	\N	\N
1577	458	User shopping cart content on Amazon.in	t	\N	\N
1578	459	Ephemeral UI state	f	\N	\N
1579	459	Application state	t	\N	\N
1580	459	System state	f	\N	\N
1581	459	None of the above	f	\N	\N
1582	460	Ajax requests on each UI change	t	\N	\N
1583	460	Periodic reloading of web-page	f	\N	\N
1584	460	Vue bindings to update data reactively	f	\N	\N
1585	460	Pure static pages with all updates rendered from server	t	\N	\N
1586	461	Ephemeral UI state	f	\N	\N
1587	461	Application state	f	\N	\N
1588	461	System state	t	\N	\N
1589	461	None of the above	f	\N	\N
1590	462	Welcome	f	\N	\N
1591	462	Welcome to iitm online degree	f	\N	\N
1592	462	App will give a warning and will show a blank page.	t	\N	\N
1593	462	None of the above	f	\N	\N
1594	463	10000 second remaining	f	\N	\N
1595	463	9999 second remaining	f	\N	\N
1596	463	9940 second remaining	t	\N	\N
1597	463	None of the above	f	\N	\N
1598	464	White, red, 2em	t	\N	\N
1599	464	Black, white, 1em	f	\N	\N
1600	464	White, white, 1em	f	\N	\N
1601	464	Black, red, 2em	f	\N	\N
1602	465	\N	f	code	const objMethods = {\r\n  zoom() {\r\n    this.fontSize += 1em\r\n  },\r\n}
1603	465	\N	f	code	const objMethods = {\r\n  zoom() {\r\n    fontSize += 1\r\n  },\r\n}
1604	465	\N	t	code	const objMethods = {\r\n  zoom() {\r\n    this.fontSize += 1\r\n  },\r\n}
1605	465	\N	f	code	const objMethods = {\r\n  zoom() {\r\n    fontSize += 1em\r\n  },\r\n}
1606	466	\N	t	code	v-if="seen", v-on:click="toggleSeen"
1607	466	\N	f	code	v-if:"seen", v-on:click:"toggleSeen"
1608	466	\N	t	code	v-if="seen", @click="toggleSeen"
1609	466	\N	f	code	v-if:"seen", @:click:"toggleSeen"
1610	467	All the progress will always be lost on the force reload of the page.	f	\N	\N
1611	467	All the progress may not necessarily be lost on the force reload of the page.	t	\N	\N
1612	467	The application will not allow force reload of the page.	f	\N	\N
1613	467	All of the above	f	\N	\N
1614	468	The system state is typically a huge collection of data.	t	\N	\N
1615	468	The user interface is dependent on the application state.	t	\N	\N
1616	468	The shopping cart of a user on an E-commerce website is an example of system state.	f	\N	\N
1617	468	All of the above	f	\N	\N
1618	469	It should be aesthetically pleasing.	f	\N	\N
1619	469	UI should be adaptive to the different screen sizes.	f	\N	\N
1620	469	UI should be intuitive to the user.	f	\N	\N
1621	469	All of the above	t	\N	\N
1622	470	In Imperative programming, all steps involved in solving the problem needs to implemented.	t	\N	\N
1623	470	In Declarative programming, all steps involved in solving the problem needs to implemented.	f	\N	\N
1624	470	In Declarative programming, only what to do needs to be declared.	t	\N	\N
1625	470	In Imperative programming, only what to do needs to be declared.	f	\N	\N
1626	471	The state of the page which is currently visible to the user is an example of application state.	f	\N	\N
1627	471	Application state is everything that is present in the memory when the app is running.	t	\N	\N
1628	471	It is completely independent of user interface.	f	\N	\N
1629	471	None of the above	f	\N	\N
1630	472	System state	t	\N	\N
1631	472	Ephemeral state	f	\N	\N
1632	472	Application state	f	\N	\N
1633	472	None of the above	f	\N	\N
1634	473	System State	t	\N	\N
1635	473	Application State	t	\N	\N
1636	473	Ephemeral State	f	\N	\N
1637	473	All of the above	f	\N	\N
1638	474	It is related to aesthetics of the application.	f	\N	\N
1639	474	It is related to typography of the content on the website.	f	\N	\N
1640	474	It is related to how user will interact with the application.	t	\N	\N
1641	474	None of the above	f	\N	\N
1642	475	It is related to aesthetics of the application.	t	\N	\N
1643	475	It is not related to aesthetics of the application.	f	\N	\N
1644	475	It is related to how the application data will be stored on the server.	f	\N	\N
1645	475	None of the above	f	\N	\N
1646	476	The state of the page which is currently visible to the user is an example of ephemeral state.	t	\N	\N
1647	476	Ephemeral state is everything that is present in the memory when the app is running.	f	\N	\N
1648	476	It is completely independent of user interface.	f	\N	\N
1649	476	None of the above	f	\N	\N
1650	477	UX design	f	\N	\N
1651	477	UI design	t	\N	\N
1652	477	Database	f	\N	\N
1653	477	None of the above	f	\N	\N
1654	478	System state	t	\N	\N
1655	478	Ephemeral state	f	\N	\N
1656	478	Application state	f	\N	\N
1657	478	None of the above	f	\N	\N
1658	479	UX design	t	\N	\N
1659	479	UI design	f	\N	\N
1660	479	Database design	f	\N	\N
1661	479	None of the above	f	\N	\N
1662	480	A	f	\N	\N
1663	480	Object	f	\N	\N
1664	480	String	t	\N	\N
1665	480	None of the above	f	\N	\N
1666	481	A	f	\N	\N
1667	481	Object	t	\N	\N
1668	481	String	f	\N	\N
1669	481	None of the above	f	\N	\N
1670	482	21	f	\N	\N
1671	482	31	t	\N	\N
1672	482	20	f	\N	\N
1673	482	30	f	\N	\N
1674	483	A task from the task queue will be pushed to the call stack only if the call stack is empty.	t	\N	\N
1675	483	A task from task queue can be pushed to the call stack even if the call stack is not empty.	f	\N	\N
1676	483	A task from the call stack will be pushed to the task queue only if task queue is empty.	f	\N	\N
1677	483	A task from the call stack can be pushed to the task queue even if the task queue is not empty.	f	\N	\N
1678	484	undefined Hello	t	\N	\N
1679	484	1 Hello	f	\N	\N
1680	484	Hello undefined	f	\N	\N
1681	484	4 Hello	f	\N	\N
1682	485	ReferenceError	f	\N	\N
1683	485	undefined	f	\N	\N
1684	485	Abhi	t	\N	\N
1685	485	None of the above	f	\N	\N
1686	486	6	f	\N	\N
1687	486	4	f	\N	\N
1688	486	9	t	\N	\N
1689	486	None of the above	f	\N	\N
1690	487	[ -9, -7, -2, 1, 2, 2, 4, 5 ]	t	\N	\N
1691	487	[ -2, -7, -9, 1, 2, 2, 4, 5 ]	f	\N	\N
1692	487	[1, 2, 2, 4, 5, -2, -7, -9]	f	\N	\N
1693	487	[ 5, 4, 2, 2, 1, -2, -7, -9 ]	f	\N	\N
1694	488	[-9, -7, -2, 1, 2, 2, 4, 5]	f	\N	\N
1695	488	[-2, -7, -9, 1, 2, 2, 4, 5]	f	\N	\N
1696	488	[1, 2, 2, 4, 5, -2, -7, -9]	f	\N	\N
1697	488	[5, 4, 2, 2, 1, -2, -7, -9]	t	\N	\N
1762	505	$y$ must be a conjugate transpose of $x$	f	\N	\N
1763	505	$y$ is equal to $x$	t	\N	\N
1764	505	$y$ must be orthogonal to $x$	t	\N	\N
1765	505	$y$ must be a scalar (possibly complex) multiple of $x$	f	\N	\N
1766	506	$0.06 - 1.97i$	f	\N	\N
1767	506	$1.54 - 1.23i$	f	\N	\N
1768	506	$1.54 + 1.23i$	t	\N	\N
1769	506	$0.8 - 0.37i$	f	\N	\N
1770	506	Not possible to calculate	f	\N	\N
1771	507	doesn't exist over $\\mathbb{R}$ but exists over $\\mathbb{C}$	t	\N	\N
1772	507	doesn't exist over $\\mathbb{C}$ but exists over $\\mathbb{R}$	f	\N	\N
1773	507	neither exists over $\\mathbb{R}$ nor exists over $\\mathbb{C}$	f	\N	\N
1774	507	exists over both $\\mathbb{C}$ and $\\mathbb{R}$	f	\N	\N
1775	508	Hermitian and Symmetric	f	\N	\N
1776	508	Symmetric but not Hermitian	f	\N	\N
1777	508	Neither Hermitian nor Symmetric	f	\N	\N
1778	508	Hermitian but not Symmetric	t	\N	\N
1779	509	True if $DD^T=I$	t	\N	\N
1780	509	False	f	\N	\N
1781	509	True if $DD^{-1}=I$	f	\N	\N
1782	510	$\\begin{bmatrix} -1 \\\\ 1+2i \\\\ 1 \\end{bmatrix}, \\begin{bmatrix} 1-2i \\\\ 6-9i \\\\ 13 \\end{bmatrix}, \\begin{bmatrix} 1+3i \\\\ -2-i \\\\ 5 \\end{bmatrix}$	t	\N	\N
1783	510	$\\begin{bmatrix} 1 \\\\ 1-2i \\\\ 1 \\end{bmatrix}, \\begin{bmatrix} 1-2i \\\\ 6-9i \\\\ 13 \\end{bmatrix}, \\begin{bmatrix} 1+3i \\\\ -2-i \\\\ 5 \\end{bmatrix}$	f	\N	\N
1784	510	$\\begin{bmatrix} -1 \\\\ 1-2i \\\\ -1 \\end{bmatrix}, \\begin{bmatrix} 1-2i \\\\ 6-9i \\\\ 13 \\end{bmatrix}, \\begin{bmatrix} 1+3i \\\\ -2-i \\\\ 5 \\end{bmatrix}$	f	\N	\N
1785	510	$\\begin{bmatrix} -1 \\\\ 1+2i \\\\ 1 \\end{bmatrix}, \\begin{bmatrix} 1-2i \\\\ 6-9i \\\\ 13 \\end{bmatrix}, \\begin{bmatrix} 1-3i \\\\ 2-i \\\\ -5 \\end{bmatrix}$	f	\N	\N
1786	511	$\\frac{1}{2}$	f	\N	\N
1787	511	1	t	\N	\N
1788	511	$-\\frac{1}{2}$	f	\N	\N
1789	511	-1	f	\N	\N
1790	511	$\\pm 1$	f	\N	\N
1791	511	$\\pm \\frac{1}{2}$	f	\N	\N
1792	512	$U = \\frac{1}{2} \\begin{bmatrix} 1+i & -1-i \\\\ \\sqrt{2} & \\sqrt{2} \\end{bmatrix}, D = \\begin{bmatrix} 1+\\sqrt{2} & 0 \\\\ 0 & 1-\\sqrt{2} \\end{bmatrix}$	t	\N	\N
1793	512	$U = \\frac{1}{4} \\begin{bmatrix} 1+i & -1-i \\\\ \\sqrt{2} & \\sqrt{2} \\end{bmatrix}, D = \\begin{bmatrix} 1+\\sqrt{2} & 0 \\\\ 0 & 1-\\sqrt{2} \\end{bmatrix}$	f	\N	\N
1794	512	$U = \\frac{1}{2} \\begin{bmatrix} -1+i & \\sqrt{2} \\\\ \\sqrt{2} & -1-i \\end{bmatrix}, D = \\begin{bmatrix} 1+\\sqrt{2} & 0 \\\\ 0 & 1-\\sqrt{2} \\end{bmatrix}$	f	\N	\N
1795	512	$U = \\frac{1}{4} \\begin{bmatrix} 1+i & \\sqrt{2} \\\\ \\sqrt{2} & 1-i \\end{bmatrix}, D = \\begin{bmatrix} -1+\\sqrt{2} & 0 \\\\ 0 & 1-\\sqrt{2} \\end{bmatrix}$	f	\N	\N
1796	513	only real eigenvalues.	f	\N	\N
1797	513	two real and two complex eigenvalue.	t	\N	\N
1798	513	three real and one complex eigenvalues.	f	\N	\N
1799	513	all complex eigenvalues	f	\N	\N
1800	514	$\\begin{bmatrix} \\cos\\theta & \\sin\\theta \\\\ -\\sin\\theta & -\\cos\\theta \\end{bmatrix}$	f	\N	\N
1801	514	$\\begin{bmatrix} \\cos\\theta & \\sin\\theta \\\\ \\sin\\theta & \\cos\\theta \\end{bmatrix}$	f	\N	\N
1802	514	$\\begin{bmatrix} -\\cos\\theta & \\sin\\theta \\\\ \\sin\\theta & \\cos\\theta \\end{bmatrix}$	t	\N	\N
1803	514	$\\begin{bmatrix} \\cos\\theta & -\\sin\\theta \\\\ \\sin\\theta & \\cos\\theta \\end{bmatrix}$	t	\N	\N
1804	514	$\\begin{bmatrix} -\\cos\\theta & \\sin\\theta \\\\ \\sin\\theta & -\\cos\\theta \\end{bmatrix}$	f	\N	\N
1805	515	$UV$ is always unitary.	f	\N	\N
1806	515	$U+V$ is always unitary.	f	\N	\N
1807	515	Both statements are true.	f	\N	\N
1808	515	Both statements are false.	f	\N	\N
1809	515	1. is false.	f	\N	\N
1810	515	2. is false.	t	\N	\N
1811	516	$\\begin{bmatrix} -1-i \\\\ 1 \\end{bmatrix}$	t	\N	\N
1812	516	$\\begin{bmatrix} -2-2i \\\\ 2 \\end{bmatrix}$	t	\N	\N
1813	516	$\\begin{bmatrix} \\frac{1+i}{2} \\\\ 1 \\end{bmatrix}$	t	\N	\N
1814	516	$\\begin{bmatrix} 1+i \\\\ 2 \\end{bmatrix}$	t	\N	\N
1815	517	True	f	\N	\N
1816	517	False	t	\N	\N
1817	518	True	t	\N	\N
1818	518	False	f	\N	\N
1819	519	$Q_1$: $n \\times m$, $Q_2$: $m \\times n$, $\\Sigma$: $n \\times n$	f	\N	\N
1820	519	$Q_1$: $n \\times n$, $Q_2$: $m \\times m$, $\\Sigma$: $n \\times m$	f	\N	\N
1821	519	$Q_1$: $m \\times n$, $Q_2$: $n \\times m$, $\\Sigma$: $m \\times m$	f	\N	\N
1822	519	$Q_1$: $m \\times m$, $Q_2$: $n \\times n$, $\\Sigma$: $m \\times n$	t	\N	\N
1823	520	The eigenvalues of $AA^T$	f	\N	\N
1824	520	The eigenvalues of $A^TA$	f	\N	\N
1825	520	Square root of the eigenvalues of $AA^T$	t	\N	\N
1826	520	Square root of the eigenvalues of $A^TA$	t	\N	\N
1827	521	$Q_2\\Sigma^T\\Sigma Q_2^T$	f	\N	\N
1828	521	$Q_1\\Sigma^T\\Sigma Q_1^T$	f	\N	\N
1829	521	$Q_2\\Sigma\\Sigma^TQ_2^T$	f	\N	\N
1830	521	$Q_1\\Sigma\\Sigma^TQ_1^T$	t	\N	\N
1831	522	$Q_1\\Sigma^T\\Sigma Q_1^T$	f	\N	\N
1832	522	$Q_2\\Sigma\\Sigma^TQ_2^T$	f	\N	\N
1833	522	$Q_2\\Sigma^T\\Sigma Q_2^T$	t	\N	\N
1834	522	$Q_1\\Sigma\\Sigma^TQ_1^T$	f	\N	\N
1835	523	only 1	f	\N	\N
1836	523	only 2	t	\N	\N
1837	523	1 and 2	f	\N	\N
1838	523	none	f	\N	\N
1839	524	$m \\times n$ and $n \\times m$	f	\N	\N
1840	524	$n \\times m$ and $m \\times n$	f	\N	\N
1841	524	$m \\times m$ and $n \\times n$	t	\N	\N
1842	524	$n \\times n$ and $m \\times m$	f	\N	\N
1843	525	unitary	f	\N	\N
1844	525	orthogonal	f	\N	\N
1845	525	real and symmetric	t	\N	\N
1846	525	diagonal	f	\N	\N
1847	526	1 and 2	f	\N	\N
1848	526	1 and 3	f	\N	\N
1849	526	2 and 3	f	\N	\N
1850	526	1 and 4	t	\N	\N
1851	527	$S=\\begin{bmatrix} 2+\\sqrt{5} & 0 \\\\ 0 & 2+\\sqrt{5} \\end{bmatrix}$	f	\N	\N
1852	527	$S=\\begin{bmatrix} 2-\\sqrt{5} & 0 \\\\ 0 & 2+\\sqrt{5} \\end{bmatrix}$	t	\N	\N
1853	527	$S=\\begin{bmatrix} 2-\\sqrt{5} & 0 \\\\ 0 & 2-\\sqrt{5} \\end{bmatrix}$	f	\N	\N
1854	527	$S=\\begin{bmatrix} -2+\\sqrt{5} & 0 \\\\ 0 & 2+\\sqrt{5} \\end{bmatrix}$	f	\N	\N
1855	528	$\\begin{bmatrix} 1 & 0 \\\\ 0 & 1 \\end{bmatrix} \\begin{bmatrix} 2\\sqrt{2} & 0 \\\\ 0 & \\sqrt{2} \\end{bmatrix} \\begin{bmatrix} \\frac{1}{\\sqrt{2}} & \\frac{1}{\\sqrt{2}} \\\\ -\\frac{1}{\\sqrt{2}} & \\frac{1}{\\sqrt{2}} \\end{bmatrix}$	t	\N	\N
1856	528	$\\begin{bmatrix} 1 & 0 \\\\ 0 & 1 \\end{bmatrix} \\begin{bmatrix} 2\\sqrt{2} & 0 \\\\ 0 & \\sqrt{2} \\end{bmatrix} \\begin{bmatrix} \\frac{1}{\\sqrt{2}} & \\frac{1}{\\sqrt{2}} \\\\ \\frac{1}{\\sqrt{2}} & \\frac{1}{\\sqrt{2}} \\end{bmatrix}$	f	\N	\N
1857	528	$\\begin{bmatrix} -1 & 0 \\\\ 0 & 1 \\end{bmatrix} \\begin{bmatrix} 2\\sqrt{2} & 0 \\\\ 0 & \\sqrt{2} \\end{bmatrix} \\begin{bmatrix} \\frac{1}{\\sqrt{2}} & \\frac{1}{\\sqrt{2}} \\\\ -\\frac{1}{\\sqrt{2}} & \\frac{1}{\\sqrt{2}} \\end{bmatrix}$	f	\N	\N
1858	528	$\\begin{bmatrix} 1 & 0 \\\\ 0 & 1 \\end{bmatrix} \\begin{bmatrix} 2\\sqrt{2} & 0 \\\\ 0 & \\sqrt{2} \\end{bmatrix} \\begin{bmatrix} \\frac{1}{\\sqrt{2}} & -\\frac{1}{\\sqrt{2}} \\\\ -\\frac{1}{\\sqrt{2}} & \\frac{1}{\\sqrt{2}} \\end{bmatrix}$	f	\N	\N
1859	529	9	f	\N	\N
1860	529	10	f	\N	\N
1861	529	11	t	\N	\N
1862	529	12	f	\N	\N
1863	530	$2ax+2by=0$ and $2bx+2cy=0$	t	\N	\N
1864	530	$\\frac{\\partial f(x,y)}{\\partial x} \\neq 0$ and $\\frac{\\partial f(x,y)}{\\partial y} \\neq 0$	f	\N	\N
1865	530	$\\frac{\\partial f(x,y)}{\\partial x}=0$ and $\\frac{\\partial f(x,y)}{\\partial y}=0$	t	\N	\N
1866	530	None of these	f	\N	\N
1867	531	1 and 2	t	\N	\N
1868	531	2 and 3	f	\N	\N
1869	531	3 and 4	f	\N	\N
1870	531	1 and 4	f	\N	\N
1871	532	$a>0$ and $ac>b^2$	t	\N	\N
1872	532	$a<0$ and $ac>b^2$	f	\N	\N
1873	532	$a=0$ and $ac=b^2$	f	\N	\N
1874	532	$a<0$ and $ac<b^2$	f	\N	\N
1875	533	$a>0$ and $ac>b^2$	f	\N	\N
1876	533	$a<0$ and $ac>b^2$	f	\N	\N
1877	533	$a>0$ and $ac=b^2$	t	\N	\N
1878	533	$a<0$ and $ac<b^2$	f	\N	\N
1879	534	$a>0$ and $ac>b^2$	f	\N	\N
1880	534	$a<0$ and $ac=b^2$	t	\N	\N
1881	534	$a>0$ and $ac=b^2$	f	\N	\N
1882	534	$a<0$ and $ac<b^2$	f	\N	\N
1883	535	$ac>b^2$	f	\N	\N
1884	535	$ac=b^2$	f	\N	\N
1885	535	$ac<b^2$	t	\N	\N
1886	536	Point $(1,0)$	f	\N	\N
1887	536	Point $(1,1)$	f	\N	\N
1888	536	Point $(0,0)$	t	\N	\N
1889	536	None of these	f	\N	\N
1890	537	It is a stationary point.	t	\N	\N
1891	537	The second order partial derivatives are always less than 0.	f	\N	\N
1892	537	The determinant of the Hessian matrix is negative.	t	\N	\N
1893	537	None of these	f	\N	\N
1894	538	are positive.	t	\N	\N
1895	538	are negative.	f	\N	\N
1896	538	may be either positive or negative.	f	\N	\N
1897	538	have unit value.	f	\N	\N
1898	539	All eigen values are positive.	t	\N	\N
1899	539	$x^TAx>0$ for all vectors $x \\neq 0$	t	\N	\N
1900	539	All pivots are positive in the reduced row echelon form.	t	\N	\N
1901	539	None of these	f	\N	\N
1902	540	is positive.	t	\N	\N
1903	540	is negative.	f	\N	\N
1904	540	may be either positive or negative.	f	\N	\N
1905	540	has unit value.	f	\N	\N
1906	541	$\\begin{bmatrix} 2 & 2 \\\\ 2 & 1 \\end{bmatrix}$	f	\N	\N
1907	541	$\\begin{bmatrix} -2 & 2 \\\\ 2 & 1 \\end{bmatrix}$	f	\N	\N
1908	541	$\\begin{bmatrix} 2 & 0 \\\\ 0 & 1 \\end{bmatrix}$	t	\N	\N
1909	541	$\\begin{bmatrix} 2 & 2 \\\\ 2 & 1 \\end{bmatrix}$	f	\N	\N
1910	542	$\\begin{bmatrix} x & y \\end{bmatrix} \\begin{bmatrix} 1 & 2 \\\\ -1 & 2 \\end{bmatrix} \\begin{bmatrix} x \\\\ y \\end{bmatrix}$	t	\N	\N
1911	542	$\\begin{bmatrix} x & y \\end{bmatrix} \\begin{bmatrix} -1 & 2 \\\\ -1 & 2 \\end{bmatrix} \\begin{bmatrix} x \\\\ y \\end{bmatrix}$	f	\N	\N
1912	542	$\\begin{bmatrix} x & y \\end{bmatrix} \\begin{bmatrix} 1 & -2 \\\\ -1 & 2 \\end{bmatrix} \\begin{bmatrix} x \\\\ y \\end{bmatrix}$	f	\N	\N
1913	542	$\\begin{bmatrix} x & y \\end{bmatrix} \\begin{bmatrix} -1 & -2 \\\\ -1 & 2 \\end{bmatrix} \\begin{bmatrix} x \\\\ y \\end{bmatrix}$	f	\N	\N
1914	543	has no stationary point	f	\N	\N
1915	543	has a stationary point at (0, 0)	t	\N	\N
1916	543	has a stationary point at (1, 1)	f	\N	\N
1917	543	has a stationary point at (-1, -1)	f	\N	\N
1918	544	positive definite	t	\N	\N
1919	544	positive semi-definite	f	\N	\N
1920	544	negative definite	f	\N	\N
1921	544	negative semi-definite	f	\N	\N
1922	545	True	t	\N	\N
1923	545	False	f	\N	\N
1924	546	(1, 1)	t	\N	\N
1925	546	(1, 2)	f	\N	\N
1926	546	(-1, 2)	f	\N	\N
1927	546	(2, -1)	f	\N	\N
1928	547	$\\begin{bmatrix} x & y & z \\end{bmatrix} \\begin{bmatrix} 1 & 0 & 1 \\\\ -1 & 1 & 1 \\\\ 0 & 0 & -1 \\end{bmatrix} \\begin{bmatrix} x \\\\ y \\\\ z \\end{bmatrix}$	f	\N	\N
1929	547	$\\begin{bmatrix} x & y & z \\end{bmatrix} \\begin{bmatrix} 1 & 0 & 1 \\\\ 1 & 1 & 1 \\\\ 0 & 0 & -1 \\end{bmatrix} \\begin{bmatrix} x \\\\ y \\\\ z \\end{bmatrix}$	f	\N	\N
1930	547	$\\begin{bmatrix} x & y & z \\end{bmatrix} \\begin{bmatrix} 1 & 0 & 1 \\\\ -1 & 1 & -1 \\\\ 0 & 0 & -1 \\end{bmatrix} \\begin{bmatrix} x \\\\ y \\\\ z \\end{bmatrix}$	f	\N	\N
1931	547	$\\begin{bmatrix} x & y & z \\end{bmatrix} \\begin{bmatrix} 1 & -1 & 1 \\\\ 1 & 0 & 1 \\\\ 1 & 1 & -1 \\end{bmatrix} \\begin{bmatrix} x \\\\ y \\\\ z \\end{bmatrix}$	t	\N	\N
1932	548	maxima.	t	\N	\N
1933	548	minima.	f	\N	\N
1934	548	saddle point.	f	\N	\N
1935	548	none of these	f	\N	\N
1936	549	positive definite.	f	\N	\N
1937	549	positive semi-definite.	f	\N	\N
1938	549	neither positive definite nor positive semi-definite.	t	\N	\N
1939	549	can not be determined	f	\N	\N
1940	550	$A$ is positive definite.	f	\N	\N
1941	550	$A$ is positive semi-definite.	f	\N	\N
1942	550	$A$ is negative definite.	t	\N	\N
1943	550	can not be determined	f	\N	\N
1944	551	$A$ is positive definite.	t	\N	\N
1945	551	$A$ is positive semi-definite.	f	\N	\N
1946	551	$A$ is neither positive definite nor positive semi-definite.	f	\N	\N
1947	551	Can not be determined	f	\N	\N
1948	552	1, 5	f	\N	\N
1949	552	3, 4	f	\N	\N
1950	552	2, 5	f	\N	\N
1951	552	1, 3	t	\N	\N
1952	553	$A = \\begin{bmatrix} \\frac{1}{\\sqrt{6}} & \\frac{-1}{\\sqrt{3}} & \\frac{1}{\\sqrt{2}} \\\\ \\frac{2}{\\sqrt{6}} & \\frac{1}{\\sqrt{3}} & 0 \\\\ \\frac{1}{\\sqrt{6}} & \\frac{-1}{\\sqrt{3}} & \\frac{-1}{\\sqrt{2}} \\end{bmatrix} \\begin{bmatrix} 2\\sqrt{2} & 0 & 0 \\\\ 0 & 2 & 0 \\\\ 0 & 0 & 0 \\end{bmatrix} \\begin{bmatrix} \\frac{1}{\\sqrt{6}} & \\frac{3}{\\sqrt{12}} & \\frac{1}{\\sqrt{12}} \\\\ \\frac{1}{\\sqrt{3}} & 0 & \\frac{-2}{\\sqrt{6}} \\\\ \\frac{1}{\\sqrt{2}} & \\frac{-1}{\\sqrt{2}} & \\frac{1}{\\sqrt{2}} \\end{bmatrix}$	t	\N	\N
1953	553	$A = \\begin{bmatrix} \\frac{1}{\\sqrt{6}} & \\frac{-1}{\\sqrt{3}} & \\frac{1}{\\sqrt{2}} \\\\ \\frac{2}{\\sqrt{6}} & \\frac{1}{\\sqrt{3}} & 0 \\\\ \\frac{1}{\\sqrt{6}} & \\frac{-1}{\\sqrt{3}} & \\frac{-1}{\\sqrt{2}} \\end{bmatrix} \\begin{bmatrix} 2\\sqrt{3} & 0 & 0 \\\\ 0 & 3 & 0 \\\\ 0 & 0 & 0 \\end{bmatrix} \\begin{bmatrix} \\frac{1}{\\sqrt{6}} & \\frac{3}{\\sqrt{12}} & \\frac{1}{\\sqrt{12}} \\\\ \\frac{1}{\\sqrt{3}} & 0 & \\frac{-2}{\\sqrt{6}} \\\\ \\frac{1}{\\sqrt{12}} & \\frac{-3}{\\sqrt{6}} & \\frac{1}{\\sqrt{24}} \\end{bmatrix}$	f	\N	\N
1954	553	$A = \\begin{bmatrix} \\frac{1}{\\sqrt{6}} & \\frac{-1}{\\sqrt{3}} & \\frac{1}{\\sqrt{2}} \\\\ \\frac{2}{\\sqrt{6}} & \\frac{1}{\\sqrt{3}} & 0 \\\\ \\frac{1}{\\sqrt{6}} & \\frac{-1}{\\sqrt{3}} & \\frac{-1}{\\sqrt{2}} \\end{bmatrix} \\begin{bmatrix} 2\\sqrt{3} & 0 & 0 \\\\ 0 & 3 & 0 \\\\ 0 & 0 & 0 \\end{bmatrix} \\begin{bmatrix} \\frac{1}{\\sqrt{6}} & \\frac{3}{\\sqrt{12}} & \\frac{1}{\\sqrt{12}} \\\\ \\frac{1}{\\sqrt{3}} & 0 & \\frac{-2}{\\sqrt{6}} \\\\ \\frac{1}{\\sqrt{2}} & \\frac{-1}{\\sqrt{2}} & \\frac{1}{\\sqrt{2}} \\end{bmatrix}$	f	\N	\N
1955	553	$A = \\begin{bmatrix} \\frac{1}{\\sqrt{6}} & \\frac{-1}{\\sqrt{3}} & \\frac{1}{\\sqrt{2}} \\\\ \\frac{2}{\\sqrt{6}} & \\frac{1}{\\sqrt{3}} & 0 \\\\ \\frac{1}{\\sqrt{6}} & \\frac{-1}{\\sqrt{3}} & \\frac{-1}{\\sqrt{2}} \\end{bmatrix} \\begin{bmatrix} 2\\sqrt{2} & 0 & 0 \\\\ 0 & 2 & 0 \\\\ 0 & 0 & 0 \\end{bmatrix} \\begin{bmatrix} \\frac{1}{\\sqrt{6}} & \\frac{3}{\\sqrt{12}} & \\frac{1}{\\sqrt{12}} \\\\ \\frac{1}{\\sqrt{3}} & 0 & \\frac{-2}{\\sqrt{6}} \\\\ \\frac{1}{\\sqrt{2}} & \\frac{-1}{\\sqrt{2}} & \\frac{1}{\\sqrt{2}} \\end{bmatrix}$	f	\N	\N
1956	554	1.618, -0.618	f	\N	\N
1957	554	1.618, 0.618	t	\N	\N
1958	554	2.618, 0.382	f	\N	\N
1959	554	2.618, -0.382	f	\N	\N
1960	555	$\\begin{bmatrix} 0.645 & -0.53 \\\\ 0.826 & 0.414 \\end{bmatrix} \\begin{bmatrix} 2.56 & 0 \\\\ 0 & 1.56 \\end{bmatrix} \\begin{bmatrix} 0.826 & -0.644 \\\\ 0.644 & 0.826 \\end{bmatrix}^T$	t	\N	\N
1961	555	$\\begin{bmatrix} 0.645 & -0.53 \\\\ -0.826 & 0.414 \\end{bmatrix} \\begin{bmatrix} 2.56 & 0 \\\\ 0 & 1.56 \\end{bmatrix} \\begin{bmatrix} 0.826 & -0.644 \\\\ 0.644 & 0.826 \\end{bmatrix}^T$	f	\N	\N
1962	555	$\\begin{bmatrix} 0.645 & -0.53 \\\\ 0.826 & 0.414 \\end{bmatrix} \\begin{bmatrix} -2.56 & 0 \\\\ 0 & 1.56 \\end{bmatrix} \\begin{bmatrix} 0.826 & -0.644 \\\\ -0.644 & 0.826 \\end{bmatrix}^T$	f	\N	\N
1963	555	$\\begin{bmatrix} -0.645 & -0.53 \\\\ 0.826 & 0.414 \\end{bmatrix} \\begin{bmatrix} 2.56 & 0 \\\\ 0 & 1.56 \\end{bmatrix} \\begin{bmatrix} 0.826 & -0.644 \\\\ 0.644 & 0.826 \\end{bmatrix}^T$	f	\N	\N
1964	556	has no stationary point.	f	\N	\N
1965	556	has a stationary point at (0, 0).	t	\N	\N
1966	556	has a stationary point at (1, 1).	f	\N	\N
1967	556	has a stationary point at (-1, -1).	f	\N	\N
1968	557	Yes, it is true	t	\N	\N
1969	557	No, it is not true	f	\N	\N
1970	558	positive definite	t	\N	\N
1971	558	positive semi-definite	f	\N	\N
1972	558	negative definite	f	\N	\N
1980	560	$\\begin{bmatrix} x & y & z \\end{bmatrix} \\begin{bmatrix} 1 & 0 & 1 \\\\ -1 & 1 & -1 \\\\ 0 & 0 & -1 \\end{bmatrix} \\begin{bmatrix} x \\\\ y \\\\ z \\end{bmatrix}$	f	\N	\N
1981	560	$\\begin{bmatrix} x & y & z \\end{bmatrix} \\begin{bmatrix} -1 & 0 & 1 \\\\ -1 & 1 & 1 \\\\ 0 & 0 & -1 \\end{bmatrix} \\begin{bmatrix} x \\\\ y \\\\ z \\end{bmatrix}$	f	\N	\N
1982	561	maxima	f	\N	\N
1983	561	minima	t	\N	\N
1984	561	saddle Point	f	\N	\N
1985	561	None of these	f	\N	\N
1986	562	$A$ is positive definite.	t	\N	\N
1987	562	$A$ is positive semidefinite.	f	\N	\N
1988	562	$A$ is neither positive definite nor positive semi-definite.	f	\N	\N
1989	562	Can not be determined.	f	\N	\N
1990	563	True	f	\N	\N
1991	563	False	t	\N	\N
1992	564	$A$ is positive definite.	t	\N	\N
1993	564	$A$ is positive semi-definite.	f	\N	\N
1994	564	$A$ is neither positive definite nor positive semi-definite.	f	\N	\N
1995	564	Can not be determined	f	\N	\N
1996	565	$3+\\sqrt{3}, 3-\\sqrt{3}$	f	\N	\N
1997	565	$\\sqrt{3+\\sqrt{3}}, \\sqrt{3-\\sqrt{3}}$	t	\N	\N
1998	565	$2+\\sqrt{2}, 2-\\sqrt{2}$	f	\N	\N
1999	565	$\\sqrt{2+\\sqrt{2}}, \\sqrt{2-\\sqrt{2}}$	f	\N	\N
2000	566	$A = \\frac{1}{\\sqrt{2}} \\begin{bmatrix} 1 & 0 & 1 & 0 \\\\ 0 & 1 & 0 & 1 \\\\ 1 & 0 & -1 & 0 \\\\ 0 & 1 & 0 & -1 \\end{bmatrix} \\begin{bmatrix} \\sqrt{3} & 0 \\\\ 0 & \\sqrt{3} \\\\ 0 & 0 \\\\ 0 & 0 \\end{bmatrix} \\begin{bmatrix} 1 & 0 \\\\ 0 & 1 \\end{bmatrix}$	f	\N	\N
2001	566	$A = \\frac{1}{\\sqrt{3}} \\begin{bmatrix} 1 & 0 & 1 & 0 \\\\ 0 & 1 & 0 & 1 \\\\ 2 & 0 & -2 & 0 \\\\ 0 & 1 & 0 & -1 \\end{bmatrix} \\begin{bmatrix} \\sqrt{2} & 0 \\\\ 0 & \\sqrt{2} \\\\ 0 & 0 \\\\ 0 & 0 \\end{bmatrix} \\begin{bmatrix} 2 & 0 \\\\ 0 & 2 \\end{bmatrix}$	f	\N	\N
2002	566	$A = \\frac{1}{\\sqrt{2}} \\begin{bmatrix} 1 & 0 & 1 & 0 \\\\ 0 & 1 & 0 & 1 \\\\ 1 & 0 & -1 & 0 \\\\ 0 & 1 & 0 & -1 \\end{bmatrix} \\begin{bmatrix} \\sqrt{2} & 0 \\\\ 0 & \\sqrt{2} \\\\ 0 & 0 \\\\ 0 & 0 \\end{bmatrix} \\begin{bmatrix} 1 & 0 \\\\ 0 & 1 \\end{bmatrix}$	t	\N	\N
2003	566	$A = \\frac{1}{\\sqrt{3}} \\begin{bmatrix} 1 & 0 & 1 & 0 \\\\ 0 & 1 & 0 & 1 \\\\ 1 & 0 & -1 & 0 \\\\ 0 & 1 & 0 & -1 \\end{bmatrix} \\begin{bmatrix} \\sqrt{3} & 0 \\\\ 0 & \\sqrt{3} \\\\ 0 & 0 \\\\ 0 & 0 \\end{bmatrix} \\begin{bmatrix} 1 & 0 \\\\ 0 & 1 \\end{bmatrix}$	f	\N	\N
\.


--
-- Data for Name: questions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.questions (id, assessment_id, heading, media_type, media_content, q_type, correct_answer) FROM stdin;
1	18	Consider a point $x = \\begin{bmatrix} 1 \\\\ -1 \\end{bmatrix}$ and a line passing through the origin which is represented by the vector $w = \\begin{bmatrix} 3 \\\\ 3 \\end{bmatrix}$. What can you say about the following quantities?\r\n(1) the projection of $x$ onto the line\r\n(2) the residue\r\n\r\n*Note: The projection is treated as a vector. The residue after the projection is also treated as a vector.*	\N	\N	mcq	\N
2	18	Consider a dataset that has $1000$ samples, where each sample belongs to $\\mathbb{R}^{30}$. PCA is run on this dataset and the top $4$ principal components are retained, the rest being discarded. If it takes one unit of memory to store a real number, find the percentage decrease in storage space of the dataset by moving to its compressed representation. \r\n\r\nEnter your answer correct to two decimal places; it should lie in the range $[0, 100]$.	\N	\N	numerical	86.2, 86.35
3	18	Consider a dataset of $100$ points all of which lie in $\\mathbb{R}^5$. The eigenvalues of the covariance matrix are given below:\r\n$3.2, 1.5, 0.2, 0.01, 0.001$\r\n\r\nIf we run the PCA algorithm on this dataset and retain the top-$k$ principal components, what is a good choice of $k$? Use the heuristic that was discussed in the lectures.	\N	\N	numerical	2
4	18	PCA is run on a dataset that has $2$ features. The resulting principal components are $w_1$ and $w_2$. We represent the points in 2D space in terms of this new coordinate system made up of the principal components. The first coordinate corresponds to $w_1$ and the second to $w_2$. \r\n\r\nIn such a scenario, what would be the sign of the coordinates for the points $P$ and $Q$?	image	img_009.png	mcq	\N
5	18	Consider a dataset that has $8$ points all of which belong to $\\mathbb{R}^2$.\n\nFind the covariance matrix of this dataset.	image	img_010.png	mcq	\N
6	18	Consider the images of points in 2D space provided below. The red line segments in one of the images represent the lengths of the residues after projecting the points on the line $L$. Which image is it?	image	\N	mcq	\N
7	18	Consider a point $P$ and a line $L$ that passes through the origin $O$. The point $R$ lies on the line.\nWe use the following notation: $w = \\vec{OR}, x = \\vec{OP}$\n\nFind the length of the projection of $x$ on the line $L$. Enter your answer correct to two decimal places.	image	img_001.png	numerical	4.9, 5.0
8	18	Consider a dataset that has $8$ points all of which belong to $\\mathbb{R}^2$.\n\nIf PCA is run on this dataset, find the variance of the dataset along the first principal component. The eigenvectors of the covariance matrix are given below:\n$\\begin{bmatrix} -0.993 \\\\ 0.115 \\end{bmatrix}, \\begin{bmatrix} -0.115 \\\\ -0.993 \\end{bmatrix}$\n\nRecall that the first principal component is the most important. Enter your answer correct to two decimal places.\n*Note: Do not try to round off or drop decimal places in the intermediate computations. If a number has 4 places after the decimal, use all of them.*	image	img_010.png	numerical	4.5, 4.6
9	18	Consider a point $P$ and a line $L$ that passes through the origin $O$. The point $R$ lies on the line.\nWe use the following notation: $w = \\vec{OR}, x = \\vec{OP}$\n\nConsider the following statements:\n\n- Statement-1: The projection of $x$ on the line $L$ is given by $(x^T w)w$\n\n- Statement-2: The projection of $x$ on the line $L$ is given by $(x^T w)x$\n\n- Statement-3: The projection of $x$ on the line $L$ is given by $(x^T x)w$\n\n- Statement-4: The projection of $x$ on the line $L$ is given by $w^T x$\n\nWhich of the above statements is true?	image	img_001.png	mcq	\N
10	20	A function $k$ is defined as follows:\r\n$k:\\mathbb{R}^d \\times \\mathbb{R}^d \\to \\mathbb{R}, k(x_1, x_2) = x_1^T x_2$\r\n\r\nIs $k$ a valid kernel?	\N	\N	mcq	\N
11	18	Consider a point $P$ and a line $L$ that passes through the origin $O$. The point $R$ lies on the line.\nWe use the following notation: $w = \\vec{OR}, x = \\vec{OP}$\n\nFind the residue after projecting $x$ on the line $L$.	image	img_001.png	mcq	\N
12	18	Consider a point $P$ and a line $L$ that passes through the origin $O$. The point $R$ lies on the line.\nWe use the following notation: $w = \\vec{OR}, x = \\vec{OP}$\n\nFind the reconstruction error for this point. Enter your answer correct to two decimal places.	image	img_001.png	numerical	4.4, 4.6
13	20	A function $k$ is defined as follows:\r\n$k:\\mathbb{R}^d \\times \\mathbb{R}^d \\to \\mathbb{R}, k(x_1, x_2) = x_1^T x_2$\r\n\r\nIf $k$ is the valid kernel, we apply it to the three-dimensional dataset to run the kernel PCA. Select the correct options.	\N	\N	mcq	\N
14	20	Consider ten data points lying on a curve of degree two in a two-dimensional space. We run a kernel PCA with a polynomial kernel of degree two on the same data points. Choose the correct options.	\N	\N	mcq	\N
15	20	Which of the following matrices can not be appropriate matrix $K=X^T X$ for some data matrix $X$?	\N	\N	mcq	\N
16	20	A function $k$ is defined as\r\n$k:\\mathbb{R}^2 \\times \\mathbb{R}^2 \\to \\mathbb{R}, k(x_1, x_2) = (x_1^T x_2)^2$\r\n\r\nIs $k$ a valid kernel?	\N	\N	mcq	\N
17	20	Kernel PCA was run on the four data points $[1,2]^T, [2,3]^T, [2,-3]^T,$ and $[4,4]^T$ with the polynomial kernel of degree 2. What will be the shape of the matrix $K$? Notations are used as per lectures.	\N	\N	mcq	\N
18	20	Kernel PCA was run on the four data points $[1,2]^T, [2,3]^T, [2,-3]^T,$ and $[4,4]^T$ with the polynomial kernel of degree 2. Find the element at the index $(2,3)$ of the matrix $K$. Take the points in the same order.	\N	\N	mcq	\N
19	20	A dataset containing 200 examples in four-dimensional space has been transformed into higher dimensional space using the polynomial kernel of degree two. What will be the dimension of transformed feature space?	\N	\N	numerical	15
20	20	Let $x_1, x_2, \\dots, x_n$ be $d$-dimensional data points ($d>n$) and $X$ be the matrix of shape $d \\times n$ containing the data points. The $k$-th largest eigenvalue and corresponding unit eigenvector of $X^T X$ is $\\lambda$ and $\\alpha_k$, respectively. What will be the projection of $x_i$ on the $k$-th principal component?	\N	\N	mcq	\N
21	20	Let $k_1$ and $k_2$ be two valid kernels. Is $3k_1 + 5k_2$ a valid kernel?	\N	\N	mcq	\N
22	21	Assume that $w_k; k=1,2,\\dots,d$ are $d$ principal components corresponding to nonzero eigenvalues of the $d$-dimensional centered data points $x_i; i=1,2,\\dots,n$.\r\nStatement 1: each $x_i$ can be written as a linear combination of $w_k$s.\r\nStatement 2: each $w_k$ can be written as a linear combination of $x_i$s.	\N	\N	mcq	\N
23	21	A transformation mapping $\\phi$ is defined as\r\n$\\phi:\\mathbb{R} \\to \\mathbb{R}^4$\r\n$\\phi(x)=[x^3, \\sqrt{3}x^2, \\sqrt{3}x, 1]^T$\r\n\r\nWhich of the following options are the same as $\\phi(x_1)^T \\phi(x_2)$ for two points $x_1, x_2 \\in \\mathbb{R}$?	\N	\N	mcq	\N
24	21	Let $C$ be the covariance matrix of $n$ data points in $d$-dimensional space. Assume that the data points are mean-centered. If $2, 5$, and $7$ are the only non-zero eigenvalues of $C$, what will be the non-zero eigenvalues of $X^T X$, where $X$ is the matrix of shape $(d,n)$ containing the data points?	\N	\N	mcq	\N
25	1	What does JAMStack stand for?	\N	\N	mcq	\N
26	1	Who coined the term “JAMStack”?	\N	\N	mcq	\N
524	75	Any $m \\times n$ matrix $A$ can be written as $A=Q_1\\Sigma Q_2^T$ the dimensions of $Q_1,Q_2$ are, respectively	\N	\N	mcq	\N
27	21	Consider an image dataset matrix $X$ of shape $(d,n)$ with $d>n$. The $k$-th principal component of the dataset can be written as $w_k = \\alpha_1 x_1 + \\alpha_2 x_2 + \\dots + \\alpha_n x_n$, where, the vector $x_i$ is the $i$-th data point. The $k$-th largest eigenvalue and the corresponding eigenvector of $X^T X$ are $4$ and $\\left[ \\frac{1}{\\sqrt{51}}, \\frac{3}{\\sqrt{51}}, \\frac{4}{\\sqrt{51}}, \\frac{5}{\\sqrt{51}} \\right]^T$, respectively.\r\n\r\nWhat will be the value of $\\alpha_1$?	\N	\N	mcq	\N
28	21	Consider an image dataset matrix $X$ of shape $(d,n)$ with $d>n$. The $k$-th principal component of the dataset can be written as $w_k = \\alpha_1 x_1 + \\alpha_2 x_2 + \\dots + \\alpha_n x_n$, where, the vector $x_i$ is the $i$-th data point. The $k$-th largest eigenvalue and the corresponding eigenvector of $X^T X$ are $4$ and $\\left[ \\frac{1}{\\sqrt{51}}, \\frac{3}{\\sqrt{51}}, \\frac{4}{\\sqrt{51}}, \\frac{5}{\\sqrt{51}} \\right]^T$, respectively.\r\n\r\nWhat will be the $k$-th largest eigenvalue of the covariance matrix $\\frac{1}{4}XX^T$? Note that $n=4$ as the length of the eigenvector of $X^T X$ is 4.	\N	\N	numerical	1
29	21	A function $k$ is defined as\r\n$k:\\mathbb{R}^2 \\times \\mathbb{R}^2 \\to \\mathbb{R}$\r\n$k([x_1, x_2]^T, [y_1, y_2]^T) = x_1^2 y_1^2 + x_2^2 y_2^2$\r\n\r\nIs $k$ a valid kernel?	\N	\N	mcq	\N
30	21	A dataset of 1000 second-hand cars has four features: kilometers driven ($x_1$), mileage ($x_2$), the present price of the car ($x_3$), and the selling price ($x_4$). The selling price seems to have the following relationship (approximate) with the other three features.\r\n$x_4 = x_1^2 x_3 + 2x_2$\r\n\r\nIf we want to project the dataset into a lower dimensional space, which of the following task would be most appropriate?	\N	\N	mcq	\N
31	21	Abhishek runs a kernel PCA on a dataset containing $n$ examples with $d$ features. Which of the following strategy he should follow to center the data points?\r\nStrategy 1: First center the dataset using the mean and then apply the kernel.\r\nStrategy 2: First apply the kernel and then center the matrix.	\N	\N	mcq	\N
32	21	A dataset containing 1000 points in 3-dimensional space is run through the kernel PCA with the polynomial kernel of degree $p$. If the transformed dataset lives in a ten-dimensional space, what will be the value of $p$?	\N	\N	numerical	2
33	21	A dataset containing 1000 examples in 10-dimensional space is projected into other dimension space using kernel PCA with the following kernel.\r\n$k(x_1, x_2) = \\exp \\left( -\\frac{||x_1 - x_2||^2}{4} \\right)$\r\n\r\nWhat will be the dimension of the projected dataset?	\N	\N	mcq	\N
34	22	Which of the following sequences is correct for K-Means algorithm?\r\n1. Assign each data point to the nearest cluster centres.\r\n2. Re-assign each point to nearest cluster centres.\r\n3. Assign cluster centres randomly.\r\n4. Re-compute cluster centres.\r\n5. Specify the number of clusters.	\N	\N	mcq	\N
35	22	If $F(z_1^t,z_2^t,\\dots,z_n^t)$ represents the value of objective function in iteration $t$ of Lloyd's algorithm, then which of the following is true?	\N	\N	mcq	\N
36	22	If $\\mu_1$ and $\\mu_2$ are means of two clusters in k-means, then the boundary between the two clusters will be	\N	\N	mcq	\N
37	22	Assume K-means is run on these points with $k = 2$. Which of the following are expected to be the clusters formed out of K-means?	image	km1.png	mcq	\N
38	22	In the initialization step of k-means++, the squared distances from the closest mean for 5 points $x_1, x_2, x_3, x_4, x_5$ are: 25, 67, 89, 24, 56. In this context, which of the following is true?	\N	\N	mcq	\N
39	22	With respect to Lloyd's algorithm, choose the correct statements:	\N	\N	mcq	\N
40	22	For 1000 data points, out of $k = 1, 10$ and $100$, which value of $k$ is likely to result in the maximum value of the objective function?	\N	\N	mcq	\N
41	22	For 100 data points, if $k = 100$, what will be the value of the objective function?	\N	\N	mcq	\N
42	22	Choose the correct statements:	\N	\N	mcq	\N
43	22	Outliers are data points that deviate significantly from the rest of data points. Knowing the way Lloyd's algorithm works, do you think it is sensitive to outliers?	\N	\N	mcq	\N
44	29	$[2, 4, -5]$ belongs to which of the following?	\N	\N	mcq	\N
45	29	Which of the following may not be an appropriate choice of loss function for regression?	\N	\N	mcq	\N
46	29	Identify which of the following requires use of classification technique.	\N	\N	mcq	\N
47	29	Mark all incorrect statements in the following	\N	\N	mcq	\N
48	29	Which of the following is false regarding supervised and unsupervised machine learning?	\N	\N	mcq	\N
49	29	The output of regression model is	\N	\N	mcq	\N
50	29	Which of the following is/are supervised learning task(s)?	\N	\N	mcq	\N
51	29	Which of the following is used for predicting a continuous target variable?	\N	\N	mcq	\N
52	29	“The is _____ used to fit the model; the _____ is used for model selection; the _____ is used for computing the generalization error.” Which of the following will fill the above blanks correctly?	\N	\N	mcq	\N
53	29	We want to learn a function $f(x)=ax+b$ which is parameterized by $(a,b)$. Using average squared error as the loss function, which of the following parameters would be best to model the given data?	\N	\N	mcq	\N
54	29	Consider the following loss functions:\n1. $\\frac{1}{n}\\sum_{i=1}^n-\\log(P(X_i))$\n\n2. $\\frac{1}{n}\\sum_{i=1}^n||g(f(X_i))-X_i||^2$\n\n3. $\\frac{1}{n}\\sum_{i=1}^n(f(X_i)-Y_i)^2$\n\n4. $\\frac{1}{n}\\sum_{i=1}^n\\mathbb{1}(f(X_i)\\neq Y_i)$\n\nThe above loss functions pertain to which of the following ML techniques (in that order)?	\N	\N	mcq	\N
55	29	Compute the loss when Pair 1 and Pair 2 (shown below) are used for dimensionality reduction. Consider the loss function to be $\\frac{1}{n}\\sum_{i=1}^n||g(f(x_i))-x_i||^2$. \n\nPair 1: $f(x)=(x_1-x_2)$, $g(u)=[u/2,u/2]$\n\nPair 2: $f(x)=(x_1+x_2)/2$, $g(u)=[u/2,u/2]$\n\nHere $f(x)$ is the encoder function and $g(x)$ is the decoder function. \n\nLoss for pair 2:\n\n| X$_{1}$ | X$_{2}$ |\n|---|---|\n| $1$ | $0.5$ |\n| $2$ | $2.3$ |\n| $3$ | $3.1$ |\n| $4$ | $3.9$ |	\N	\N	numerical	3.61,4
56	29	What will be the amount of loss when the functions $g=3x_1+1$ and $h=2x_1+2$ are used to represent the regression line. Consider the average squared error as loss function. \n\nLoss for g:\n\n| X | Y |\n|---|---|\n| $[2]$ | $5.8$ |\n| $[3]$ | $8.3$ |\n| $[6]$ | $18.3$ |\n| $[7]$ | $21$ |\n| $[8]$ | $22$ |	\N	\N	numerical	2.82,3.11
57	29	What will be the amount of loss when the functions $g=3x_1+1$ and $h=2x_1+2$ are used to represent the regression line. Consider the average squared error as loss function. \n\nLoss for h:\n\n| X | Y |\n|---|---|\n| $[2]$ | $5.8$ |\n| $[3]$ | $8.3$ |\n| $[6]$ | $18.3$ |\n| $[7]$ | $21$ |\n| $[8]$ | $22$ |	\N	\N	numerical	11.32,12.52
58	29	What will be the average misclassification error when the functions $g(X)=\\text{sign}(x_1-x_2-2)$ and $h(X)=\\text{sign}(x_1+x_2-10)$ are used to classify the data points into classes $+1$ or $-1$. \r\n\r\n| X | y |\r\n|---|---|\r\n| $[4,2]$ | $+1$ |\r\n| $[8,4]$ | $+1$ |\r\n| $[2,6]$ | $-1$ |\r\n| $[4,10]$ | $-1$ |\r\n| $[10,2]$ | $+1$ |\r\n| $[12,8]$ | $-1$ |\r\n\r\nLoss for h:	\N	\N	numerical	0.475,0.525
525	75	For any real $m \\times n$ matrix $A$, $AA^T$ is	\N	\N	mcq	\N
59	29	$f(x_1,x_2,x_3)=\\frac{x_1+2x_2}{2}$ is used as encoder function and $g(u)=[u,2u,3u]$ is used as decoder function for dimensionality reduction of following data set. Give the reconstruction error for this encoder decoder pair. The reconstruction error is the mean of the squared distance between actual input and reconstructed input.\n\n| X |\n|---|\n| $[1,2,3]$ |\n| $[2,3,4]$ |\n| $[-1,0,1]$ |\n| $[0,1,1]$ |	\N	\N	numerical	32.78,36.22
60	29	What will be the average misclassification error when the functions $g(X)=\\text{sign}(x_1-x_2-2)$ and $h(X)=\\text{sign}(x_1+x_2-10)$ are used to classify the data points into classes $+1$ or $-1$. \n\n| X | Y |\n|---|---|\n| $[4,2]$ | $+1$ |\n| $[8,4]$ | $+1$ |\n| $[2,6]$ | $-1$ |\n| $[4,10]$ | $-1$ |\n| $[10,2]$ | $+1$ |\n| $[12,8]$ | $-1$ |\n\nLoss for g:	\N	\N	numerical	0.158,0.175
62	1	What does PWA stand for in the context of an app?	\N	\N	mcq	\N
63	1	What does SPA stand for in the context of an app?	\N	\N	mcq	\N
64	1	What is the default port number used by a flask application?	\N	\N	mcq	\N
65	5	Consider the following variable declaration. What will be printed on console for console.log(x.value)?	code	let x = {}	mcq	\N
66	10	Which of the following shows the correct output, if the program written below is executed?	code	let a = [2, 3, 4];\r\nlet b = [2, 2, ...a, 5];\r\nlet c = b.find(x => x % 2);\r\nconsole.log(c);	mcq	\N
67	10	Which of the following shows the correct output, if the program written below is executed?	code	let a = {\r\n    'first_name' : 'abhi',\r\n    'age' : 22,\r\n    'place' : 'delhi'\r\n};\r\n\r\nlet { first_name : alt } = a;\r\nconsole.log(first_name);	mcq	\N
68	10	What will be the output of the following program?	code	arr = ['iitmonline', true, 3, (a, b) => a + b]\r\nlet result = Array()\r\nfor (let i = 0; i < arr.length; i++) {\r\n    result.push(typeof arr[i])\r\n}\r\nconsole.log(result)	mcq	\N
69	10	What will be the output of the following program?	code	arr = ['iitmonline', true, 3, (a, b) => a + b]\r\nlet result = Array()\r\nfor (const i in arr) {\r\n    result.push(arr[i] * arr[i])\r\n}\r\nconsole.log(result)	mcq	\N
70	10	What will be the output of the following program?	code	fruit = {\r\n    name: 'Apple',\r\n    color: 'red',\r\n}\r\n\r\nlet description = ({ name, color, shape = 'Spherical' }) => {\r\n    console.log(`NULL is NULL and NULL`)\r\n}\r\n\r\ndescription(fruit)	mcq	\N
71	10	What will be the output of the following program?	code	class Player {\r\n    constructor(name) {\r\n        this.name = name\r\n        this.team = 'Indian Cricket Team'\r\n        this.nationality = 'Indian'\r\n    }\r\n}\r\n\r\nclass Bowler extends Player {\r\n    constructor(name, wicket, average) {\r\n        super(name)\r\n        this.role = 'Bowler'\r\n        this.wicket = wicket\r\n        this.average = average\r\n    }\r\n}\r\n\r\nbumbum = new Bowler('Jasprit Bumrah', 101, 22.79)\r\nconsole.log(bumbum)	mcq	\N
72	10	What will be the output of the following program?	code	class Player {\r\n    constructor(name, team) {\r\n        this.name = name\r\n        this.team = team\r\n    }\r\n\r\n    get describe() {\r\n        return `NULL from NULL is a NULL`\r\n    }\r\n}\r\n\r\nclass Batsman extends Player {\r\n    constructor(name, team) {\r\n        super(name, team)\r\n        this.role = 'Batsman'\r\n    }\r\n}\r\n\r\np = new Batsman('Rohit', 'Indian Cricket Team')\r\nconsole.log(p.describe)	mcq	\N
73	10	What will be the output of the following program?	code	const obj = {\r\n    a: 10,\r\n    operation(x, y, n) {\r\n        return x ** n + y + this.a\r\n    },\r\n}\r\n\r\nconst arr = Array()\r\np = obj.operation\r\n\r\narr.push(p.bind(obj, 2)(3, 2))\r\narr.push(p.apply(obj, [2, 2, 3, 4, 5]))\r\narr.push(p.call(obj, 2, 3, 4))\r\n\r\nconsole.log(arr)	mcq	\N
74	10	What will be the output of the following program?	code	const obj = {\r\n    firstName: 'Narendra',\r\n    lastName: 'Mishra',\r\n\r\n    get fName() {\r\n        return this.firstName\r\n    },\r\n\r\n    get lName() {\r\n        return this.lastName\r\n    },\r\n\r\n    set lName(name) {\r\n        this.lastName = name\r\n    },\r\n}\r\n\r\nobj.lName = 'Mourya'\r\nobj.lName = console.log(obj.lName)	mcq	\N
75	10	Which of the following programs will generate an error, if executed?	code	#Code snippet 1:\nfor (const i = 1; i <= 5; i++) {\n    console.log(i)\n}\n\n#Code snippet 2:\nfor (const i in [1, 2, 3, 4, 5]) {\n    console.log(i)\n}	mcq	\N
76	29	Compute the loss when Pair 1 and Pair 2 (shown below) are used for dimensionality reduction. Consider the loss function to be $\\frac{1}{n}\\sum_{i=1}^n||g(f(x_i))-x_i||^2$. \n\nPair 1: $f(x)=(x_1-x_2)$, $g(u)=[u/2,u/2]$\n\nPair 2: $f(x)=(x_1+x_2)/2$, $g(u)=[u/2,u/2]$\n\nHere $f(x)$ is the encoder function and $g(x)$ is the decoder function. \n\nLoss for pair 1:\n\n| X$_{1}$ | X$_{2}$ |\n|---|---|\n| $1$ | $0.5$ |\n| $2$ | $2.3$ |\n| $3$ | $3.1$ |\n| $4$ | $3.9$ |	\N	\N	numerical	15,16
77	31	Regarding a $d$-dimensional vector $x$, which of the following four options is not equivalent to the rest three options?	\N	\N	mcq	\N
78	31	$f(x) = \\begin{cases} 3x+3, & \\text{if } x \\geq 3 \\\\ 2x+8, & \\text{if } x < 3 \\end{cases}$\r\n\r\nWhich of the following is/are true?	\N	\N	mcq	\N
79	31	Approximate the value of $e^{0.011}$ by linearizing $e^x$ around $x=0$.	\N	\N	numerical	1,1.02
80	31	Approximate $\\sqrt{3.9}$ by linearizing $\\sqrt{x}$ around $x=4$.	\N	\N	numerical	1.96,2.0
81	31	Which of the following pairs of vectors are perpendicular to each other?	\N	\N	mcq	\N
82	31	What is the linear approximation of $f(x,y)=x^3+y^3$ around (2, 2)?	\N	\N	mcq	\N
83	31	What is the gradient of $f(x,y)=x^3y^2$ at (1, 2)?	\N	\N	mcq	\N
84	31	The gradient of $f=x^3+y^2+z^3$ at $x=0$, $y=1$ and $z=1$ is given by	\N	\N	mcq	\N
85	31	The directional derivative of $f(x,y,z)=x^3+y^2+z^3$ at (1, 1, 1) in the direction of unit vector along $v=[1,-2,1]$ is (correct upto three decimal places)	\N	\N	numerical	0.775,0.856
86	31	The direction of steepest ascent for the function $2x+y^3+4z$ at the point $(1,0,1)$ is	\N	\N	mcq	\N
87	31	The directional derivative of $f(x,y,z)=x+y+z$ at $(-1,1,0)$ in the direction of unit vector along [1, -1, 1] is (correct upto three decimal places)	\N	\N	numerical	0.548,0.605
88	31	Which of the following is the equation of the line passing through $[7,8,6]$ in the direction of vector $[1,2,3]$	\N	\N	mcq	\N
89	31	Which of the following functions is/are continuous?	\N	\N	mcq	\N
90	31	For two vectors $a$ and $b$, which of the following is true as per Cauchy-Schwarz inequality?\n(i) $a^Tb \\leq ||a||*||b||$\n\n(ii) $a^Tb \\geq -||a||*||b||$\n\n(iii) $a^Tb \\geq ||a||*||b||$\n\n(iv) $a^Tb \\leq -||a||*||b||$	\N	\N	mcq	\N
91	32	Let $f(x) = \\begin{cases} \\frac{\\sin(x)}{x}, & x \\neq 0 \\\\ 1, & x = 0 \\end{cases}$\r\n\r\nIs $f(x)$ continuous at $x=0$?	text	\N	mcq	\N
92	32	If $U=[10,100]$, $A=[30,50]$ and $B=[50,90]$, which of the following is/are false?\r\n\r\n(Consider all values to be integers)	text	\N	mcq	\N
93	32	Two $d$-dimensional vectors $x$ and $y$ and the following terms:\r\n\r\n(i) $x^Ty$\r\n\r\n(ii) $x \\cdot y$\r\n\r\n(iii) $\\sum_{i=1}^d x_i y_i$\r\n\r\nWhich of the above terms are equivalent?	\N	\N	mcq	\N
94	32	The linear approximation of $\\tan(x)$ around $x=0$ is:	text	\N	mcq	\N
95	32	The partial derivative of $x^3+y^2$ w.r.t. $x$ at $x=1$ and $y=2$ is	\N	\N	numerical	3
96	32	$f(x) = \\begin{cases} 7x+2, & \\text{if } x > 1 \\\\ 9, & \\text{if } x \\leq 1 \\end{cases}$\r\n\r\nIs $f(x)$ continuous?	\N	\N	mcq	\N
97	2	Which of the following is the correct way to embed an applet in an HTML document, assuming that the java byte code file “appletdemo.class” is kept in the same directory as the HTML document?	\N	\N	mcq	\N
98	2	Which of the following is the correct usage of “alt” attribute in the <applet> tag in an HTML document?	\N	\N	mcq	\N
99	2	Which of the following statements is true regarding JavaScript?	\N	\N	mcq	\N
100	32	The best approximation of $e^{0.019}$? (Use linear approximation around 0).	\N	\N	mcq	\N
101	32	The linear approximation of $f(x,y)=x^2+y^2$ around $(1, 1)$ is:	\N	\N	mcq	\N
102	32	The gradient of $f(x,y)=x^2y$ at $(1, 3)$ is:	\N	\N	mcq	\N
103	32	The directional derivative of $f(x,y,z)=x^2+3y+z^2$ at $(1, 2, 1)$ along the unit vector in the direction of $[1, -2, 1]$ is (correct upto three decimal places)	\N	\N	numerical	-0.856,-0.775
104	32	The direction of steepest ascent for the function $x^2+y^3+z^4$ at point $(1, 1, 1)$ is:	text	\N	mcq	\N
105	32	The directional derivative of $f(x,y,z)=x+y+z$ at point $[-1, 1, -1]$ along the unit vector in the direction of $[1, -1, 1]$ is (correct upto three decimal places)	\N	\N	numerical	0.548,0.605
106	32	The vector equation/s of a line that passes through $[1, 2, 3]$ and $[4, 0, 1]$:\r\n\r\n(i) $[x,y,z]=[1,2,3]+\\alpha[3,-2,-2]$\r\n\r\n(ii) $[x,y,z]=[4,0,1]+\\alpha[-3,2,2]$\r\n\r\n(iii) $[x,y,z]=[1,2,3]+\\alpha[4,0,1]$\r\n\r\n(iv) $[x,y,z]=[4,0,1]+\\alpha[1,2,3]$	\N	\N	mcq	\N
107	32	As per Cauchy-Schwarz inequality, if $b$ is a negative scalar multiple of $a$, then:	text	\N	mcq	\N
108	9	Which of the following shows the correct output, if the program written below is executed?	code	let a = [75, 55, 22, 5];\r\nconsole.log(a.sort());	mcq	\N
109	2	Which of the following can be considered as advantage(s) of JavaScript language?	\N	\N	mcq	\N
110	2	Which of the following is true regarding java applet?	\N	\N	mcq	\N
111	2	Which of the following web browsers, evolved from Netscape Navigator?	\N	\N	mcq	\N
112	8	Which of the following statements is not true regarding JavaScript?	\N	\N	mcq	\N
113	8	What will be the output on console if the following JavaScript program is executed using command line?	code	{\n    let x = 5;\n}\nconsole.log(x)	mcq	\N
114	8	What is AJAX?	\N	\N	mcq	\N
115	8	Consider the following variable declaration. What will be printed on console for console.log(x)?	code	let x	mcq	\N
116	8	Consider the following code snippet. What will be the output of console.log(x)?	code	const x = 14\r\nx = 15	mcq	\N
117	8	Consider the following JavaScript program, What will be the output of the statement: console.log(obj.color)?	code	const obj = {\n    color: 'red',\n    changeColor: function (color) {\n        this.color = color\n    },\n}\n\nobj.changeColor('Yellow')	mcq	\N
118	8	Which of the following is/are correct way(s) to define a function in JavaScript?	\N	\N	mcq	\N
119	8	Consider the following HTML document. What will be the background color of an element having ID ‘div1’ in the rendered webpage corresponding to this document?	code	<!DOCTYPE html>\n<html lang=""en"">\n<head>\n    <meta charset=""UTF-8"" />\n    <script>\n        document.getElementById('div1').style.backgroundColor = 'yellow';\n    </script>\n    <title>Document</title>\n</head>\n<body>\n    <div\n        id=""div1""\n        style=""height: 100px; width: 100px; background-color: red""\n    ></div>\n</body>\n</html>"\n	mcq	\N
120	8	Consider the following HTML document. What will be the background color of an element having ID ‘div’ after 6 seconds?	code	<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8" />\n    <title>Document</title>\n</head>\n<body>\n    <div\n        id="div"\n        style="background-color: black; height: 50px; width: 50px"\n    ></div>\n    <script>\n        const colors = {\n            color1: 'red',\n            color2: 'green',\n            color3: 'yellow',\n        }\n        let i = 1\n        let color = null\n        setInterval(() => {\n            if (i % 2 != 0) {\n                color = colors.color1\n            }\n            else if (i % 4 == 0) {\n                color = colors.color2\n            }\n            else {\n                color = colors.color3\n            }\n            document.getElementById('div').style.backgroundColor = color\n            i++\n        }, 1000)\n    </script>\n</body>\n</html>	mcq	\N
121	3	Which of the following encoding does a JavaScript engine use in general?	\N	\N	mcq	\N
122	3	What will be the output on console if the following JavaScript program is executed using command line?	code	{\r\n    var x = 5;\r\n}\r\nconsole.log(x)	mcq	\N
123	3	Which of the following operators is used to avoid coercion in JavaScript language?	\N	\N	mcq	\N
124	3	Which of the following have a block-level scope in JavaScript language?	\N	\N	mcq	\N
125	3	What is ECMAScript?	\N	\N	mcq	\N
126	4	Which of the following is not a reserve word in JavaScript language?	\N	\N	mcq	\N
127	4	Which of the following is not a valid literal in JavaScript?	\N	\N	mcq	\N
128	4	Which of the following is not a primitive data type in the JavaScript language?	\N	\N	mcq	\N
129	4	Which of the following is not a reserved word in JavaScript?	\N	\N	mcq	\N
130	4	Which of the following is true regarding primitive data types in JavaScript?	\N	\N	mcq	\N
131	5	Consider the following variable declaration. What will be printed on console for console.log(x)?	code	let x = {}	mcq	\N
132	9	Which of the following shows the correct output, if the program written below is executed?	code	const a = {\n  name: 'Abhi',\n  age: 22\n};\n\nb = [];\nfor (let i = 0; i < 3; i++){\n  b.push({...a})\n}\nb[1].name = 'Akshay';\nconsole.log(b[0].name);	mcq	\N
133	9	Which of the following shows the correct output, if the program written below is executed?	code	a = {\n  name: 'Abhi',\n  age: 22\n};\n\nb = [];\nfor (let i = 0; i < 3; i++){\n  b.push(a)\n}\n\nb[1].name = 'Akshay';\nconsole.log(b[0].name);	mcq	\N
134	9	What will be the output of the program?	code	x = [1, 2, 3, 4, 5, 6]\ny = [...x, 7, 8, 9]\nz = y.filter((x) => x % 2 == 0)\n     .map((i) => i * i)\n     .reduce((a, i) => a + i, (a = 0))\nconsole.log(z)	mcq	\N
135	9	What will be the output of the following program?	code	const ePowerx = {\n  x: 1,\n  n: 1,\n  set parameters(param) {\n    param = param.split(' ')\n    this.x = param[0]\n    this.n = param[1]\n  },\n  get uptoNterms() {\n    let result = 1\n    let y = 1\n    for (let i = 1; i < this.n; i++) {\n      y = y * this.x\n      result = result + y\n    }\n    return result\n  },\n}\nePowerx.parameters = '2 3'\nconsole.log(ePowerx.uptoNterms)	mcq	\N
136	9	What will be the output of the following program?	code	const course = {\n  courseName: 'Modern Application Development 2',\n  courseCode: 'mad2',\n}\n\nconst student = {\n  __proto__: course,\n  studentName: 'Rakesh',\n  studentCity: 'Delhi',\n}\n\nconst { courseName } = student\nconsole.log(courseName)	mcq	\N
138	9	What will be the output of the following program?	code	api = { A: 'Application', P: 'Programming', I: 'Interface' }\nconst standsFor = (x) => {\n  for (const [k, v] of Object.entries(api)) {\n    if (k != x) {\n      return v\n    }\n  }\n}\n\nconsole.log(standsFor('A'))	mcq	\N
139	5	What will be the output, if the JavaScript program written below is executed?	code	const x\r\nconsole.log(x)	mcq	\N
140	5	Consider the following code snippet. What will be the output of console.log(x)?	code	let x = 14\r\nx = 15	mcq	\N
141	5	Consider the following JavaScript program. What will be the output for the statement: console.log(obj.color)?	code	const obj = {color: 'red'}\r\n\r\nobj.changeColor = function (color) {this.color = color}\r\n\r\nobj.changeColor('green')	mcq	\N
142	6	Which of the following is not a frontend framework for web development?	\N	\N	mcq	\N
143	6	Which of the following is not a backend framework for web development?	\N	\N	mcq	\N
144	6	Which of the following is correct regarding JavaScript?	\N	\N	mcq	\N
145	6	What does AJAX stand for?	\N	\N	mcq	\N
146	23	Which of the following is true about machine learning?	\N	\N	mcq	\N
147	23	Which of the following tasks is more suitable for traditional programming than machine learning?	\N	\N	mcq	\N
148	23	Which among these is not a machine learning problem?	\N	\N	mcq	\N
149	23	The traditional programming approach for a given task may fail in cases where:	\N	\N	mcq	\N
150	24	Which of these is better suited to be solved using regression?	\N	\N	mcq	\N
151	24	Regression is used when the output variable is:	\N	\N	mcq	\N
152	25	Which of the following is/are type(s) of supervised learning techniques?	\N	\N	mcq	\N
153	25	Regression is a type of:	\N	\N	mcq	\N
154	25	Which of the following functions corresponds to a regression model?	\N	\N	mcq	\N
155	25	In supervised learning, the training labels are available.	\N	\N	mcq	\N
156	25	Supervised learning is essentially	\N	\N	mcq	\N
157	26	Classification models are _______	\N	\N	mcq	\N
158	26	Which of the following loss functions can be applied to a classification model?	\N	\N	mcq	\N
159	26	We evaluate our model on which of the following data?	\N	\N	mcq	\N
160	26	Model selection is done using which of the following data?	\N	\N	mcq	\N
161	27	Unsupervised learning is essentially	\N	\N	mcq	\N
162	27	Let $$f: \\mathbb{R}^d \\to \\mathbb{R}^{d'}$$ be an encoder function for dimensionality reduction. What is the typical relation between $$d$$ and $$d'$$?	\N	\N	mcq	\N
163	27	Let $$f: \\mathbb{R}^{d'} \\to \\mathbb{R}^d$$ be a decoder function for dimensionality reduction. What is the typical relation between $$d$$ and $$d'$$?	\N	\N	mcq	\N
164	27	For the data $$\\{X_1, X_2, \\dots, X_n\\}$$ where $$X_i \\in \\mathbb{R}^d$$, $$f: \\mathbb{R}^d \\to \\mathbb{R}^{d'}$$ (encoder), and $$g: \\mathbb{R}^{d'} \\to \\mathbb{R}^d$$ (decoder), which of the following is the correct loss function?	\N	\N	mcq	\N
165	27	Which of the following come under unsupervised learning?	\N	\N	mcq	\N
166	28	The input data for an unsupervised learning algorithm is of the form (Note: $$X_i$$ and $$Y_i$$ are vectors, $$y_i$$ are scalars):	\N	\N	mcq	\N
167	28	Which of the following gives a probabilistic model?	\N	\N	mcq	\N
168	28	Which of the following is the correct loss function for density estimation?	\N	\N	mcq	\N
169	28	During parameter estimation for a density estimation method such as Gaussian Mixture Model, which of the following is minimized?	\N	\N	mcq	\N
170	30	Which of the following is true about a model?	\N	\N	mcq	\N
171	30	Identify which of the following problem requires regression algorithm.	\N	\N	mcq	\N
172	30	For spam detection, if we use traditional programming rather than a machine learning approach, which problems may be faced?	\N	\N	mcq	\N
173	30	In a regression model, the parameters $$w$$ and $$b$$ are:	\N	\N	mcq	\N
174	30	Identify classification problem(s) in the following statements	\N	\N	mcq	\N
175	30	Identify task that needs the use of regression in the following	\N	\N	mcq	\N
176	30	Which of the following are examples of unsupervised learning problems?	\N	\N	mcq	\N
177	30	Which of the following is/are incorrect?	\N	\N	mcq	\N
178	30	Which of the following functions corresponds to a classification model?	\N	\N	mcq	\N
179	30	Which of the following can form a good encoder decoder pair for $$d$$ dimensional data?	\N	\N	mcq	\N
180	30	Consider Scenario 1 (Cancer detection) and Scenario 2 (Mobile Sales).	\N	\N	mcq	\N
181	30	Consider the data set in the image where each data point has features $$x_1, x_2, x_3$$. We want to reduce dimension from 3 to 1.\n\n**Pair 1:**\n$$f(x_1, x_2, x_3) = x_1 - x_2 + x_3$$\n$$g(u) = [u, u, u]$$\n\nCalculate the reconstruction loss for Pair 1.	image	pic/image_6edda2.png	numerical	2.95,3.05
182	30	Consider the data set in the image where each data point has features $$x_1, x_2, x_3$$. We want to reduce dimension from 3 to 1.\n\n**Pair 2:**\n$$\\tilde{f}(x_1, x_2, x_3) = \\frac{x_1 + x_2 + x_3}{3}$$\n$$\\tilde{g}(u) = [u, u, u]$$\n\nCalculate the reconstruction loss for Pair 2.	image	pic/image_6edda2.png	numerical	0.63,0.7
183	7	Which of the following keywords can be used to declare a variable with global scope?	\N	\N	mcq	\N
184	7	Which of the following statements is true regarding JavaScript language?	\N	\N	mcq	\N
185	7	Which of the following statement(s) is/are correct regarding JavaScript?	\N	\N	mcq	\N
186	7	What will be the output of the following program?	code	const obj = {\r\n  name: 'Rohit',\r\n  changeName: function (name) {\r\n    this.name = name\r\n  },\r\n}\r\n\r\nobj.changeName('Mohit')\r\nconsole.log(obj.name)	mcq	\N
187	7	Consider the following code snippet. What will be the output of console.log(x.name)?	code	const x = { name: 'rohit' }\r\nx.name = 'Mohit'	mcq	\N
188	7	What will be the output of the following program?	code	const obj = {\r\n  name: 'Rohit',\r\n  changeName: (name) => {\r\n    this.name = name\r\n  },\r\n}\r\n\r\nobj.changeName('Mohit')\r\nconsole.log(obj.name)	mcq	\N
189	7	What will be the output of the following program?	code	const obj = {\r\n  name: 'Rohit',\r\n  arrowFunction: null,\r\n  normalfunction: function () {\r\n    this.arrowFunction = () => {\r\n      console.log(this.name)\r\n    }\r\n  },\r\n}\r\n\r\nobj.normalfunction()\r\nobj.arrowFunction()	mcq	\N
190	7	Which of the following is correct output for the following code snippet?	code	setTimeout(() => console.log('hello from setTimeOut one'), 0)\r\nconsole.log('hello for main one')\r\nsetTimeout(() => console.log('hello from setTimeOut two'), 0)\r\nconsole.log('hello from main two')	mcq	\N
191	7	Consider the following HTML document. What will be the background color of an element having ID 'div1' in the rendered webpage corresponding to this document?	code	<!DOCTYPE html>\r\n<html lang="en">\r\n<head>\r\n  <meta charset="UTF-8" />\r\n  <script>\r\n    setTimeout(() => {\r\n      document.getElementById('div1').style.backgroundColor = 'yellow'\r\n    }, 0)\r\n  </script>\r\n  <title>Document</title>\r\n</head>\r\n<body>\r\n  <div\r\n    id="div1"\r\n    style="height: 100px; width: 100px; background-color: red"\r\n  ></div>\r\n</body>\r\n</html>	mcq	\N
192	7	Consider the following JavaScript program. What will be the last value shown on the console after 4 seconds?	code	let startNamePrinter = (name) => {\r\n  let x = name.split('').reverse()\r\n  let handler = setInterval(() => {\r\n    let y = x.pop()\r\n    console.log(y)\r\n  }, 1000)\r\n\r\n  setTimeout(() => {\r\n    clearInterval(handler)\r\n  }, (name.length + 1) * 1000)\r\n}\r\n\r\nstartNamePrinter('orange')	mcq	\N
193	11	What are some of the most important types of data that machine learning models deal with?	\N	\N	mcq	\N
194	11	Map the dataset on the left to the domain on the right:	\N	| Dataset | Domain |\n| :--- | :--- |\n| (1) Record of all IPL matches played so far | (a) Finance |\n| (2) Credit profile of customers | (b) E-Commerce |\n| (3) 3D structure of proteins | (c) Bioinformatics |\n| (4) Click-stream data of Amazon consumers | (d) Sports analytics |\n\nWe could define a machine learning problem associated with each dataset on the left.	mcq	\N
195	11	E-commerce recommendations were discussed briefly in the lecture. When a customer visits a website to buy a product, which of the following are important features that a recommendation system should take into account while making its recommendation?	\N	\N	mcq	\N
196	11	Can you think of domains other than e-commerce where recommendations play an important role?	\N	\N	mcq	\N
197	11	You are given the data of marks scored by students in a class in a csv file. Your task is to find the class topper. Is this a machine learning problem?	\N	\N	mcq	\N
198	11	In the previous problem, you have access to a dataset. Consider the following claim: "Data is an important aspect of any machine learning problem. So, every problem that has a dataset associated with it can be classified as a machine learning problem." What is wrong with this claim?	\N	\N	mcq	\N
199	12	What are some of the broad paradigms of machine learning discussed in the lecture?	\N	\N	mcq	\N
200	12	Which of the following scenarios can be modeled as a binary classification problem?	\N	\N	mcq	\N
201	12	For every mail that comes to your inbox, you have to design an algorithm that can assign exactly one of these four labels to it:\r\n- family\r\n- friends\r\n- work\r\n- spam\r\n\r\nWhat type of machine learning problem does this correspond to?	\N	\N	mcq	\N
202	12	Assume that you find yourself in the following scenarios:\n\n* **Scenario-1:** You are given a bucket of red and blue balls. Someone commands you to separate them into two separate buckets of uniform color.\n* **Scenario-2:** You are given a bucket of black balls that look identical, but weigh differently. There is no one around you to tell you what to do. However, you try to separate the balls into different buckets, such that balls in a given bucket have more or less the same weight.\n\nIf a machine were to be trained to do these actions, what paradigms of machine learning would they correspond to?	\N	\N	mcq	\N
203	13	Is the following statement true or false:\r\nCompression is the act of throwing away a fraction of data-points from the dataset.	\N	\N	mcq	\N
204	13	Consider the following dataset:\r\n\r\n$$ \\left\\{ \\begin{bmatrix} 1 \\\\ 2 \\\\ 3 \\\\ 4 \\end{bmatrix}, \\begin{bmatrix} 1 \\\\ 5 \\\\ 3 \\\\ 0 \\end{bmatrix}, \\begin{bmatrix} -1 \\\\ -2 \\\\ 0 \\\\ 0 \\end{bmatrix}, \\begin{bmatrix} -1 \\\\ 2 \\\\ -3 \\\\ 4 \\end{bmatrix}, \\begin{bmatrix} -1 \\\\ 5 \\\\ 9 \\\\ -4 \\end{bmatrix} \\right\\} $$\r\n\r\nIf $$n$$ represents the number of data-points and $$d$$ represents the number of features, what are the values of $$n$$ and $$d$$?	\N	\N	mcq	\N
205	13	Consider the following dataset?\r\n\r\n$$ \\left\\{ \\begin{bmatrix} 3 \\\\ 6 \\\\ -3 \\end{bmatrix}, \\begin{bmatrix} 5 \\\\ 10 \\\\ -5 \\end{bmatrix}, \\begin{bmatrix} -2 \\\\ -4 \\\\ 2 \\end{bmatrix}, \\begin{bmatrix} 0 \\\\ 0 \\\\ 0 \\end{bmatrix} \\right\\} $$\r\n\r\nWhich of the following vectors could be chosen as a representative for the above dataset?	\N	\N	mcq	\N
206	13	Consider the following dataset in $$\\mathbb{R}^2$$:\r\n\r\n$$ \\left\\{ \\begin{bmatrix} 1 \\\\ 2 \\end{bmatrix}, \\begin{bmatrix} 2 \\\\ 4 \\end{bmatrix}, \\begin{bmatrix} -3 \\\\ -6 \\end{bmatrix}, \\begin{bmatrix} 0 \\\\ 0 \\end{bmatrix} \\right\\} $$\r\n\r\nIf we use a representative and the corresponding coefficients to come up with an alternative representation of the points, what would be the reconstruction error for this dataset?	\N	\N	numerical	0
207	13	You have a dataset of $$100$$ points in $$\\mathbb{R}^3$$ where all of them lie on a line passing through the origin. You wish to choose a representative $$w$$ for this dataset such that $$||w||=1$$. How many representatives can be chosen?	\N	\N	mcq	\N
208	13	Let $$w$$ be a vector that represents a line $$L$$ passing through the origin. What is the projection of a point $$x$$ onto this line? Note that $$||w||$$ is not necessarily equal to $$1$$.	\N	\N	mcq	\N
209	14	Consider the following dataset and two lines $$L_1$$ and $$L_2$$:\r\n\r\nWhich of the two lines is a good choice for a compressed representation of the dataset and why?	image	pic/img_004.png	mcq	\N
210	14	Which of the following expressions is the reconstruction error for a dataset of $$n$$ points, with respect to a line passing through the origin represented by the vector $$w$$. Note that $$||w||=1$$. (Select all that apply)	\N	\N	mcq	\N
211	14	Is the following statement true or false?\r\nThe reconstruction error is always a non-negative scalar quantity.	\N	\N	mcq	\N
212	14	Select all formulations of the optimization problem that are equivalent to the one given below:\r\n\r\n$$ \\min_{w, ||w||=1} \\frac{1}{n} \\sum_{i=1}^{n} -(x_i^T w)^2 $$	\N	\N	mcq	\N
213	14	Given a dataset of $$n$$ points in $$\\mathbb{R}^d$$, what is the dimension of the covariance matrix?	\N	\N	mcq	\N
214	14	What is the optimal value of $$w$$ for the optimization problem posed towards the end of the lecture?	\N	\N	mcq	\N
215	15	Consider the following figure:\r\n\r\nThe line shown in the figure is obtained after one round of running the "possible algorithm". Does a second round seem necessary here?	image	pic/img_005.png	mcq	\N
216	15	Which of the following represents the expression for the residue of a point $$x$$ after projecting it onto a line passing through the origin, represented by $$w$$? Note that $$||w||=1$$.	\N	\N	mcq	\N
217	15	We are given a dataset of $$n$$ points in $$\\mathbb{R}^d$$ and a line passing through the origin that is represented by $$w$$.\r\n\r\n**S1:** The residue corresponding to every point is perpendicular to $$w$$.\r\n**S2:** All the residues are collinear, that is, they lie on a line (passing through the origin).	\N	\N	mcq	\N
218	15	Is the following dataset centered?\r\n\r\n$$ \\left\\{ \\begin{bmatrix} 1 \\\\ 2 \\\\ -1 \\end{bmatrix}, \\begin{bmatrix} 0 \\\\ 0 \\\\ 0 \\end{bmatrix}, \\begin{bmatrix} -1 \\\\ -2 \\\\ 1 \\end{bmatrix}, \\begin{bmatrix} 0 \\\\ 1 \\\\ 2 \\end{bmatrix}, \\begin{bmatrix} 1 \\\\ -1 \\\\ -2 \\end{bmatrix}, \\begin{bmatrix} -1 \\\\ 0 \\\\ 0 \\end{bmatrix} \\right\\} $$	\N	\N	mcq	\N
219	16	$$w_1$$ is the line which minimizes the reconstruction error of a set of points and $$w_2$$ is the line which minimizes the reconstruction error of the residues. What is the value of $$w_1^T w_2$$?	\N	\N	numerical	0
220	16	$$B=\\{w_1, \\dots, w_d\\}$$ is a set of $$d$$ orthonormal vectors in $$\\mathbb{R}^d$$ that are obtained by running the algorithm for $$d$$ rounds on some centered dataset. Select all correct statements.	\N	\N	mcq	\N
221	16	Consider a dataset of $$1000$$ points, each of which belongs to $$\\mathbb{R}^5$$. If you know nothing else about the dataset to begin with, what is the number of rounds of the algorithm after which the residues completely vanish?	\N	\N	numerical	5
222	16	Consider a dataset of $$1000$$ points, each of which belongs to $$\\mathbb{R}^{10}$$. Upon running the algorithm on this dataset, the residues completely vanish after $$4$$ rounds. Which of the following statements is true?	\N	\N	mcq	\N
223	17	What is the best line one can obtain in the $$k^{\\text{th}}$$ round of the algorithm?	\N	\N	mcq	\N
224	17	What is the value of the following expression if $$\\lambda_k$$ is an eigenvalue of the covariance matrix $$C$$ for eigenvector $$w_k$$?\r\n\r\n$$ w_k^T C w_k $$	\N	\N	mcq	\N
225	17	Given a dataset of $$n$$ points, $$x_1, \\dots, x_n$$, the $$k^{\\text{th}}$$ eigenvector and the corresponding eigenvalue of the covariance matrix are $$w_k$$ and $$\\lambda_k$$ respectively. Consider the following statements:\r\n\r\n**S1:** $$ \\lambda_k = \\frac{1}{n} \\sum_{i=1}^{n} (x_i^T w_k)^2 $$\r\n**S2:** $$ \\lambda_k $$ is non-negative	\N	\N	mcq	\N
226	17	Given a centered dataset of $$n$$ points, $$x_1, \\dots, x_n$$, and a line $$w$$ that passes through the origin, consider the following set of quantities:\r\n\r\n$$ \\{x_1^T w, \\dots, x_n^T w\\} $$\r\n\r\nWhat is the average of the quantities in the above set?	\N	\N	numerical	0
227	17	Consider the following dataset and two lines $$L_1$$ and $$L_2$$:\r\n\r\nWhich of the two lines is a good direction for a compressed representation of the dataset and why?	image	pic/img_006.png	mcq	\N
228	19	An image is a collection of pixels. A pixel is stored as a float value and typically occupies 4 bytes of memory. Consider a dataset of $$1000$$ images, where each image has dimensions $$100 \\times 100$$. Approximately, how much memory does the entire dataset occupy?	\N	\N	mcq	\N
229	19	Consider a dataset that has $$100$$ points that belong to $$\\mathbb{R}^3$$. All of them are found to lie on a line that passes through the origin. We use a unit vector along the line as a representative and the coefficients with respect to it to represent the individual data-points. Compute the percentage decrease in the size of the dataset if we move to this new representation. Assume that it takes one unit of space to store one feature. Enter your answer correct to two decimal places; it should be in the range $$[0, 100]$$.	\N	\N	numerical	65,66
230	19	Consider the following dataset that has four points, all of which lie on a line:\r\n    \r\n$$ S = \\left\\{ \\begin{bmatrix} 0 \\\\ 0 \\end{bmatrix}, \\begin{bmatrix} 3 \\\\ 4 \\end{bmatrix}, \\begin{bmatrix} 6 \\\\ 8 \\end{bmatrix}, \\begin{bmatrix} 1/5 \\\\ 4/15 \\end{bmatrix} \\right\\} $$\r\n\r\nAmong the vectors given below, choose a representative that has unit length.	\N	\N	mcq	\N
231	19	Consider the following dataset that has four points, all of which lie on a line:\r\n\r\n$$ S = \\left\\{ \\begin{bmatrix} 0 \\\\ 0 \\end{bmatrix}, \\begin{bmatrix} 3 \\\\ 4 \\end{bmatrix}, \\begin{bmatrix} 6 \\\\ 8 \\end{bmatrix}, \\begin{bmatrix} 1/5 \\\\ 4/15 \\end{bmatrix} \\right\\} $$\r\n\r\nUsing the unit length representative vector $$ \\begin{bmatrix} 3/5 \\\\ 4/5 \\end{bmatrix} $$, compute the coefficients for these four points. The $$i^{\\text{th}}$$ element from the left in each option is the coefficient for the $$i^{\\text{th}}$$ element from the left in the set $$S$$.	\N	\N	mcq	\N
232	19	Consider the following image. $$P$$ is a point in 2D space. $$Q$$ is a proxy for this point on a line passing through the origin. The image is drawn to scale.\r\n\r\nWhich of the following is the error vector?	image	pic/img_007.png	mcq	\N
233	19	Consider the following image. $$P$$ is a point in 2D space. $$Q$$ is a proxy for this point on a line passing through the origin. The image is drawn to scale.\r\n\r\nIs $$Q$$ the "best" representation of $$P$$ on the line?	image	pic/img_007.png	mcq	\N
234	19	Consider the following image. $$P$$ is a point in 2D space. $$Q$$ is a proxy for this point on a line passing through the origin. The image is drawn to scale.\r\n\r\nIf $$Q'$$ is the "best" representation of $$P$$ on the line, then which of the following statements are true? Notation: $$|\\vec{AB}|$$ is the length of the vector $$\\vec{AB}$$.	image	pic/img_007.png	mcq	\N
235	19	Is the following statement true or false?\r\n\r\nThe projection of $$x$$ onto $$w$$ was derived to be $$(x^T w)w$$, where $$w$$ is a unit vector. Since this derivation was done for the special case of 2D vectors, this formula is not applicable in the general case of $$d$$-dimensional vectors.	\N	\N	mcq	\N
236	19	Consider a mean-centered dataset of $$n$$ points where each point belongs to $$\\mathbb{R}^d$$. $$w_1, \\dots, w_k$$ are the first $$k$$ principal components obtained by running PCA on the dataset, where $$k < d$$. The following relationship is observed:\r\n    \r\n$$ x_i - \\left[ \\sum_{j=1}^{k} (x_i^T w_j)w_j \\right] = 0, \\quad 1 \\leq i \\leq n $$\r\n\r\nWhich of the following statement about the dataset is true?	\N	\N	mcq	\N
237	19	In the context of PCA, given $$n$$ data-points in $$\\mathbb{R}^d$$ that are mean-centered, after estimating $$w_1$$ in the first round, what is the mean of the residues?	\N	\N	mcq	\N
238	19	Consider two ways of representing $$n$$ datapoints that belong to $$\\mathbb{R}^d$$ in the form of a matrix:\r\n* **Approach-1:** A matrix $$X_1$$ of dimension $$n \\times d$$\r\n* **Approach-2:** A matrix $$X_2$$ of dimension $$d \\times n$$\r\n\r\nAssume that the dataset is mean-centered. Select all correct expressions for the covariance matrix.	\N	\N	mcq	\N
239	19	Consider a mean-centered dataset obtained from the banking domain that has $$100$$ data-points, each of which is described by $$7$$ features. The dataset is represented as a $$100 \\times 7$$ matrix, $$X$$. You run PCA on this dataset and observe that the residues vanish completely after $$k$$ iterations.\r\n\r\nA little later, a domain expert makes the following observations. If $$c_i$$ represents the $$i^{\\text{th}}$$ column of $$X$$, then:\r\n\r\n(1) The set of vectors $$c_1, c_2, c_3, c_4$$ are linearly independent.\r\n\r\n(2) The following relations are satisfied:\r\n\r\n* (a) $$c_5 = c_1 + c_3$$\r\n* (b) $$c_6 = 2c_3 - 3c_4$$\r\n* (c) $$c_7 = c_2 + 3c_4$$\r\n\r\nWhat is the value of $$k$$? Assume that the dataset is already mean-centered.	\N	\N	numerical	4
240	19	Consider the following image:\r\n\r\nHere, $$w$$ is a vector and $$L$$ is a line perpendicular to $$w$$ that passes through the origin. $$R_1$$ and $$R_2$$ are two regions on either side of the line $$L$$. If $$x$$ is an arbitrary vector in the plane, select all correct statements.	image	pic/img_008.png	mcq	\N
241	33	What is the type of the following expression?	code	1 + 4 / 2	mcq	\N
242	33	What is the type of the following expression?	code	(1 > 0) and (-1 < 0) and (1 == 1)	mcq	\N
243	33	Convert the following mathematical statement into a Python expression.\r\n\r\n10³ + 9³ = 12³ + 1³ = 1729	\N	\N	mcq	\N
244	33	E_1 and E_2 are Boolean values. Consider the following expression.\nWhat can you say about the value printed by the code given above?	code	E_3 = not (E_1 or E_2)\r\nE_4 = (not E_1) and (not E_2)\r\nE_3 == E_4	mcq	\N
245	33	E is a boolean variable. Consider the following sequence of expressions:\r\n\r\nThis pattern keeps repeating for a thousand lines. If line number 500 evaluates to False, what is the value of E?	code	not E\r\nnot not E\r\nnot not not E\r\nnot not not not E\r\n.\r\n.\r\n.	mcq	\N
246	33	For what values of a and b does the following expression evaluate to True? Assume that both a and b are positive integers.\r\n\r\nEnter the value of a.	code	word = '138412345678901938'\r\nword[a:b] == '123456789'	numerical	4
247	33	For what values of a and b does the following expression evaluate to True? Assume that both a and b are positive integers.\r\n\r\nEnter the value of b.	code	word = '138412345678901938'\r\nword[a:b] == '123456789'	numerical	13
248	33	We need to write a program that performs this task: accept two names (strings) as input. Print True if the first name comes before the second in alphabetical order, and False otherwise.\n\n**Sample test cases:**\n\n| Input 1 | Input 2 | Output |\n| :--- | :--- | :--- |\n| sachin | rohit | False |\n| saina | sindhu | True |\n\nFor example, sachin comes after rohit, so the expected output is False. Assume that all names consist of just one word and will be entered in lower case during the time of input. Select all correct implementations of this program.	\N	\N	mcq	\N
249	33	What is the output of the following snippet of code?	code	x = 2 ** 5\r\nx1 = x // 2\r\nx2 = x1 // 2\r\nx3 = x2 // 2\r\nx4 = x3 // 2\r\nx5 = x4 // 2\r\nprint(x1 + x2 + x3 + x4 + x5)	numerical	31
250	34	What will be the output of the following statement?	code	print('15 % 3 * 2 + 2')	mcq	\N
251	34	What will be the output of the following statement?	code	print("a + 'b' + c + '' + d")	mcq	\N
252	34	A snippet of code gives the following output when executed:	\N	\n```1 2 3 4 5```\n\nThere is exactly one space between any two consecutive integers. Which of the following options correspond to the correct code snippet?	mcq	\N
253	34	What will be the type of the following expressions?\n\n(A) float\n\n(B) int\n\n(C) str\n\n(D) bool	code	13 % 5 // 2 * 30 ** 5\r\n"@Python"\r\n20 ** 10 / 2 + 25 - 70\r\n(5 > 3) and False\r\n20 * 100.0 // 11 % 5	mcq	\N
254	34	Given a string variable `word` that stores some word in the English language, we wish to create a new string with just two characters:\n\n- The first character in the new string is the first letter in `word`.\n- The second character in the new string is the last letter in `word`.\n\nAssume that `word` has at least three characters. Which of the following lines of code can be used to create the new string?	\N	\N	mcq	\N
255	34	Consider the following snippet of code. \nWhat is the output of the code for the following input?\n```\n10\n11\n12\n\n	code	x = int(input())\r\ny = int(input())\r\nz = int(input())\r\navg = (x + y + z) / 3\r\nprint(avg)	mcq	\N
256	34	Consider the following snippet of code. \nWhat is the output of the code for the following input?\n```\n10\n20	code	w1 = input()\r\nw2 = input()\r\nprint(w1 + w2)	numerical	1020
257	34	What is the output? What do you think is happening here?	code	2 ** 3 ** 0	numerical	2
258	36	Which of the following are valid names for variables in Python?	\N	\N	mcq	\N
260	36	Assume that `a`, `b` and `c` are three distinct integers. The following code runs without any error.\n\nSelect all statements that evaluate to `True` at the end of execution of the code given above. 	code	x, y, z = a, b, c\r\nx = y = z	mcq	\N
261	36	`x` is a variable of type `float` and is of the form `a.bcd`, where `a, b, c, d` are all positive integers less than 10. What is the output of the following snippet of code?	code	print(int(x))\r\nprint(int(-x))	mcq	\N
262	36	Consider the following code blocks:\r\n\r\nTwo blocks of code are said to be equivalent if they produce the same output for a given input. Are the two blocks equivalent?	code	#Block-1\nflag = True\nif flag == True:\n    print('works')\n\n#Block-2\nflag = True\nif flag:\n    print('works')	mcq	\N
263	36	Consider the following code-blocks. `E` is a Boolean expression. Two blocks of code are said to be equivalent if they produce the same output for a given input. Select all true statements.	code	#Block-1\nif E:\n    print('good')\nelse:\n    print('bad')\n\n#Block-2\nif E:\n    print('good')\nprint('bad')\n\n#Block-3\nprint('good')\nprint('bad')	mcq	\N
264	36	`bool_var` is a variable of type `bool`. `x` is a variable of type `int`. Assume that both these variables have already been defined. Now, consider the following code-block:\r\n\r\nWhich of the following statements are true at the end of execution of the code-block given above? 	code	if bool_var:\r\n    x = x + 1\r\n    bool_var = not bool_var\r\n    if bool_var:\r\n        x = x + 1\r\n    else:\r\n        x = x - 1\r\nprint(x)	mcq	\N
265	36	Consider the following code-block. `E_1`, `E_2` and `E_3` are all Boolean variables that have already been defined. `x` is a variable that has NOT been defined before. \r\n\r\nWhen will this code throw an error?	code	if E_1:\r\n    x = 1\r\nif E_2:\r\n    x = 2\r\nif E_3:\r\n    x = 3\r\nprint(x)	mcq	\N
266	36	Consider the following code-block. `E_1`, `E_2` and `E_3` are all Boolean variables that have already been defined. `x` is a variable that has NOT been defined before. \n\nIf the code throws an error, in which line will it occur? Enter an integer between 1 and 7, both endpoints included.	code	if E_1:\r\n    x = 1\r\nif E_2:\r\n    x = 2\r\nif E_3:\r\n    x = 3\r\nprint(x)	numerical	7
267	36	Select the correct code snippet that prints a backslash character to the console.	\N	\N	mcq	\N
268	36	Consider the following snippet of code:\n\nIf the output of this code is the string `This is a valid name`, select all possible inputs to the program.	code	# Warning! This code may not make complete sense for certain inputs!\r\nname = input()\r\nif name.isalpha():\r\n    print('This is a valid name')\r\nelse:\r\n    print('This is not a valid name')	mcq	\N
269	36	What is the output?	code	alphabets = 'abcdefghijklmnopqrstuvwxyz'\r\neven = alphabets[0: 10: 2]\r\nprint(even)	mcq	\N
270	36	Consider the following snippet of code. What is the output of this code for the following input?\n\n**Input:**\n`1234`	code	a, b, c, d = input()\r\nprint(a)\r\nprint(b)\r\nprint(c)\r\nprint(d)	mcq	\N
271	35	A word is termed valid if the output of the following code is `True` when the word is given as the input to the code. \n\nSelect all valid words from the options given below. 	code	word = input()\r\nvalid = False\r\n# both 'a' and 'z' are in lower case\r\nif 'a' <= word[0] <= 'z':\r\n    if word[0] == word[-1]:\r\n        valid = True\r\nprint(valid)	mcq	\N
272	35	A word is termed valid if the output of the following code is `True` when the word is given as the input to the code. \r\n\r\nGoing by the code given, under what conditions can a word be termed valid?	code	word = input()\r\nvalid = False\r\n# both 'a' and 'z' are in lower case\r\nif 'a' <= word[0] <= 'z':\r\n    if word[0] == word[-1]:\r\n        valid = True\r\nprint(valid)	mcq	\N
273	35	Consider the following snippet of code. Assume that `L` is a positive integer that has already been defined at this stage.\n\nThe code is run twice, with two different input words. Each input word is a string that consists only of letters without any spaces in them.\n\n**Output-1:**\n`short good`\n\n**Output-2:**\n`long goodnessme`\n\nWith just this data given to you, what is the value of `L`? 	code	# L is a positive integer that has already been defined at this stage\r\nword = input()\r\nspace = ' ' # there is a single space\r\nif len(word) < L:\r\n    word = 'short' + space + word\r\nelif L <= len(word) < 2 * L:\r\n    word = 'medium' + space + word\r\nelse:\r\n    word = 'long' + space + word\r\nprint(word)	numerical	5
274	35	A three digit number is called a sandwich number if the sum of its first and last digit is equal to its middle digit. Accept a three digit number as input and print `sandwich` if the number is a sandwich number. Print `plain` if the number is not a sandwich number. \r\n\r\nSelect the correct implementation of the code that achieves this.	\N	\N	mcq	\N
275	35	Consider the following snippet of code. What will be the value of **X** in the output for the given input? \n\n**Input:**\n```\n-1\n4\n1\n```\n\n**Output:**\n```\nPX\nNY\n```	code	x = int(input())\r\ny = int(input())\r\nz = int(input())\r\n\r\n# Block-1 Start\r\nif x > 0 or y > 0 or z > 0:\r\n    if (x > 0 and y > 0) or (y > 0 and z > 0) or (z > 0 and x > 0):\r\n        if x > 0 and y > 0 and z > 0:\r\n            print('P3')\r\n        else:\r\n            print('P2')\r\n    else:\r\n        print('P1')\r\n# Block-1 End\r\n\r\n# Block-2 Start\r\nif x < 0 or y < 0 or z < 0:\r\n    if (x < 0 and y < 0) or (y < 0 and z < 0) or (z < 0 and x < 0):\r\n        if x < 0 and y < 0 and z < 0:\r\n            print('N3')\r\n        else:\r\n            print('N2')\r\n    else:\r\n        print('N1')\r\n# Block-2 End	numerical	2
276	35	Consider the following snippet of code. What will be the value of **Y** in the output for the given input? \n\n**Input:**\n```\n-1\n4\n1\n```\n\n**Output:**\n```\nPX\nNY\n```	code	x = int(input())\r\ny = int(input())\r\nz = int(input())\r\n\r\n# Block-1 Start\r\nif x > 0 or y > 0 or z > 0:\r\n    if (x > 0 and y > 0) or (y > 0 and z > 0) or (z > 0 and x > 0):\r\n        if x > 0 and y > 0 and z > 0:\r\n            print('P3')\r\n        else:\r\n            print('P2')\r\n    else:\r\n        print('P1')\r\n# Block-1 End\r\n\r\n# Block-2 Start\r\nif x < 0 or y < 0 or z < 0:\r\n    if (x < 0 and y < 0) or (y < 0 and z < 0) or (z < 0 and x < 0):\r\n        if x < 0 and y < 0 and z < 0:\r\n            print('N3')\r\n        else:\r\n            print('N2')\r\n    else:\r\n        print('N1')\r\n# Block-2 End	numerical	1
277	35	Consider the following snippet of code. When does the code given print no value?	code	x = int(input())\r\ny = int(input())\r\nz = int(input())\r\n\r\n# Block-1 Start\r\nif x > 0 or y > 0 or z > 0:\r\n    if (x > 0 and y > 0) or (y > 0 and z > 0) or (z > 0 and x > 0):\r\n        if x > 0 and y > 0 and z > 0:\r\n            print('P3')\r\n        else:\r\n            print('P2')\r\n    else:\r\n        print('P1')\r\n# Block-1 End\r\n\r\n# Block-2 Start\r\nif x < 0 or y < 0 or z < 0:\r\n    if (x < 0 and y < 0) or (y < 0 and z < 0) or (z < 0 and x < 0):\r\n        if x < 0 and y < 0 and z < 0:\r\n            print('N3')\r\n        else:\r\n            print('N2')\r\n    else:\r\n        print('N1')\r\n# Block-2 End	mcq	\N
278	35	Consider the following snippet of code. Is the following statement True or False?\n\nFor any combination of inputs x, y and z at least one `else` statement will be executed.	code	x = int(input())\r\ny = int(input())\r\nz = int(input())\r\n\r\n# Block-1 Start\r\nif x > 0 or y > 0 or z > 0:\r\n    if (x > 0 and y > 0) or (y > 0 and z > 0) or (z > 0 and x > 0):\r\n        if x > 0 and y > 0 and z > 0:\r\n            print('P3')\r\n        else:\r\n            print('P2')\r\n    else:\r\n        print('P1')\r\n# Block-1 End\r\n\r\n# Block-2 Start\r\nif x < 0 or y < 0 or z < 0:\r\n    if (x < 0 and y < 0) or (y < 0 and z < 0) or (z < 0 and x < 0):\r\n        if x < 0 and y < 0 and z < 0:\r\n            print('N3')\r\n        else:\r\n            print('N2')\r\n    else:\r\n        print('N1')\r\n# Block-2 End	mcq	\N
279	35	Select the correct implementation of a piece of code that accepts a sentence as input and prints the number of words in it. \r\n\r\nA sentence is just a sequence of words with a space between consecutive words. You can assume that the sentence will not have any other punctuation marks. You can also assume that the input string will have at least one word.	\N	\N	mcq	\N
280	35	Consider the following snippet of code. What should be the input to this code to get the following output?\r\n\r\n**Output:**\r\n```text\r\nStudent record: \r\n    Dept: ABC\r\n    Name: MR FNAME LNAME\r\n    Roll No: 999\r\n    Library Card No: AX999\r\n```	code	dept    = input()\r\ncourse  = input()\r\nprefix  = input()\r\nname    = input()\r\nroll_no = input()\r\nname = prefix + " " + name.upper() # one space\r\nlib_id = dept[0] + course[0] + roll_no\r\nprint("Student record:")\r\nindent = '    ' # four spaces\r\nprint(indent + "Dept:", dept)\r\nprint(indent + "Name:", name)\r\nprint(indent + "Roll No:", roll_no)\r\nprint(indent + "Library Card No:", lib_id)	mcq	\N
281	35	Consider the following snippet of code. Select all possible inputs for which this code prints `PERFECT!` as output.	code	word = input()\r\nmatch = False\r\nif word.count('(') == word.count(')'):\r\n    if word.count('[') == word.count(']'):\r\n        if word.count('{') == word.count('}'):\r\n            match = True\r\nif match:\r\n    print('PERFECT!')\r\nelse:\r\n    print('IMPERFECT!')	mcq	\N
282	9	What will be the output of the following program?	code	const obj = {\n  x: 1,\n  y: 1,\n  set nums(xCommay) {\n    numbers = xCommay.split(', ')\n    this.x = numbers[0]\n    this.y = numbers[1]\n  },\n  get nums() {\n    return this.x + ', ' + this.y\n  },\n  xPowery: function () {\n    let result = 1\n    for (let i = 1; i <= this.y; i++) {\n      result = result * this.x\n    }\n    return result\n  },\n}\nobj.nums = '2,3'\nconsole.log(obj.xPowery())	mcq	\N
526	75	Any $m \\times n$ matrix $A$ can be written as $A=Q_1\\Sigma Q_2^T$. Consider the following statements:\r\n\r\n1. eigen vectors of $AA^T$ go into $Q_1$\r\n2. eigen vectors of $AA^T$ go into $Q_2$\r\n3. eigen vectors of $A^TA$ go into $Q_1$\r\n4. eigen vectors of $A^TA$ go into $Q_2$	\N	\N	mcq	\N
527	76	Which of the following matrices are similar to $A=\\begin{bmatrix} 1 & 2 \\\\ 2 & 3 \\end{bmatrix}$?	\N	\N	mcq	\N
528	76	SVD of $A=\\begin{bmatrix} 2 & 2 \\\\ -1 & 1 \\end{bmatrix}$ is	\N	\N	mcq	\N
529	77	The partial derivative of $f(x,y)=x^2+3xy+2y^2$ with respect to $y$ at (1,2) is	\N	\N	mcq	\N
530	77	The function $f(x,y)=ax^2+2bxy+cy^2$ has a stationary point at point $(p,q)$ if	\N	\N	mcq	\N
531	77	$(x_0,y_0)$ is a stationary point of $f(x,y)$ if\r\n\r\n1. $\\frac{\\partial f}{\\partial x}=0$ at $(x_0,y_0)$\r\n2. $\\frac{\\partial f}{\\partial y}=0$ at $(x_0,y_0)$\r\n3. $\\frac{\\partial f}{\\partial x} \\neq 0$ at $(x_0,y_0)$\r\n4. $\\frac{\\partial f}{\\partial y} \\neq 0$ at $(x_0,y_0)$	\N	\N	mcq	\N
532	77	A function $f(x,y)=ax^2+2bxy+cy^2$ is positive definite if	\N	\N	mcq	\N
533	77	A function $f(x,y)=ax^2+2bxy+cy^2$ is positive semi-definite if	\N	\N	mcq	\N
534	77	A function $f(x,y)=ax^2+2bxy+cy^2$ is negative semi-definite if	\N	\N	mcq	\N
535	77	A function $f(x,y)=ax^2+2bxy+cy^2$ has a saddle point at $(0,0)$ if	\N	\N	mcq	\N
536	77	Which of the following is a stationary point for the function $f(x,y)=ax^2+2bxy+cy^2$, where $a,b,c$ are positive integers?	\N	\N	mcq	\N
537	77	Which of the following is/are true characteristics of a saddle point?	\N	\N	mcq	\N
538	78	The eigenvalues of a positive definite matrix	\N	\N	mcq	\N
539	78	For a positive definite matrix $A$, which of the following is/are valid?	\N	\N	mcq	\N
540	78	The determinant of a positive definite matrix	\N	\N	mcq	\N
541	78	Which of the following matrices is/are positive definite?	\N	\N	mcq	\N
542	78	What is the correct representation of $x^2+xy+2y^2$ in the matrix form?	\N	\N	mcq	\N
543	79	The function $f(x,y)=2xy+y^2$	\N	\N	mcq	\N
544	79	The matrix $A=\\begin{bmatrix} 4 & 1 & -1 \\\\ 1 & 2 & 1 \\\\ -1 & 1 & 2 \\end{bmatrix}$ is	\N	\N	mcq	\N
545	79	The matrix $A=\\begin{bmatrix} 6 & 2 \\\\ 2 & 1 \\end{bmatrix}$ is positive definite.	\N	\N	mcq	\N
546	79	The function $f(x,y)=4+x^3+y^3-3xy$ has a stationary point at	\N	\N	mcq	\N
547	79	The correct representation of $x^2-z^2+2yz+2xz$ in the matrix form is	\N	\N	mcq	\N
548	79	Given a function $f(x,y)=-3x^2-6xy-6y^2$, the point $(0,0)$ is a _______	\N	\N	mcq	\N
549	79	The matrix $\\begin{bmatrix} 6 & 5 \\\\ 5 & 4 \\end{bmatrix}$ is	\N	\N	mcq	\N
550	79	Select all the statements that are true about the $A=\\begin{bmatrix} -6 & 0 & 0 \\\\ 0 & -5 & 0 \\\\ 0 & 0 & -7 \\end{bmatrix}$	\N	\N	mcq	\N
551	79	A matrix 2x2 $A$ has determinant $8$ and trace $6$. Which of the following are true about the matrix?	\N	\N	mcq	\N
552	79	The singular values of a matrix $A=\\begin{bmatrix} 1 & 2 \\\\ 2 & 1 \\end{bmatrix}$ are	\N	\N	mcq	\N
553	79	The SVD of the matrix $A=\\begin{bmatrix} 0 & 1 & 1 \\\\ 2 & 2 & 0 \\\\ 0 & 1 & 1 \\end{bmatrix}$ is	\N	\N	mcq	\N
554	79	Find the singular values of $A=\\begin{bmatrix} 1 & 0 \\\\ 1 & 1 \\end{bmatrix}$	\N	\N	mcq	\N
555	79	The SVD of matrix $A=\\begin{bmatrix} 2 & 0 \\\\ 1 & 2 \\end{bmatrix}$ is	\N	\N	mcq	\N
556	80	The function $f(x,y)=x^2+y^2$	\N	\N	mcq	\N
557	80	If $A=\\begin{bmatrix} 4 & 2 \\\\ 2 & 2 \\end{bmatrix}$ and $B=\\begin{bmatrix} 1 & 1 \\\\ 1 & 2 \\end{bmatrix}$ then $A+B$ is a positive definite matrix. Is this statement true?	\N	\N	mcq	\N
558	80	The matrix $A=\\begin{bmatrix} 2 & -1 & 1 \\\\ -1 & 2 & -1 \\\\ 1 & -1 & 2 \\end{bmatrix}$ is	\N	\N	mcq	\N
559	80	The function $f(x,y)=2x^2+2xy+2y^2-6x$ has a stationary point at	\N	\N	mcq	\N
560	80	The correct representation of $x^2+y^2-z^2-xy+yz+xz$ in the matrix form is	\N	\N	mcq	\N
561	80	Given $f(x,y)=3x^2+4xy+2y^2$, the point $(0,0)$ is a _________	\N	\N	mcq	\N
562	80	Which of the following statements are true about the matrix $A=\\begin{bmatrix} 4 & 2 \\\\ 2 & 3 \\end{bmatrix}$	\N	\N	mcq	\N
563	80	The matrix $A=\\begin{bmatrix} 1 & 2 \\\\ 2 & 1 \\end{bmatrix}$ is positive definite	\N	\N	mcq	\N
564	80	Which of the following statement is true about the matrix $A=\\begin{bmatrix} 3 & 0 & 0 \\\\ 0 & 5 & 0 \\\\ 0 & 0 & 7 \\end{bmatrix}$?	\N	\N	mcq	\N
565	80	The non-zero singular values of the matrix $A=\\begin{bmatrix} 1 & 1 & 0 \\\\ 1 & 0 & 1 \\\\ 0 & 0 & 0 \\\\ 1 & 1 & 0 \\end{bmatrix}$ are	\N	\N	mcq	\N
566	80	The SVD of the matrix $A=\\begin{bmatrix} 1 & 0 \\\\ 0 & 1 \\\\ 1 & 0 \\\\ 0 & 1 \\end{bmatrix}$ is	\N	\N	mcq	\N
61	9	Assuming that the index.html, module1.js, and module2.js are kept inside the same directory, then what will be the background color, height and width of the HTML element having ID 'div1', if rendered using a browser?	code	#index.html\n<!DOCTYPE html>\n<html lang="en">\n  <head>\n    <meta charset="UTF-8" />\n    <title>Document</title>\n    <script src="module1.js" type="module"></script>\n  </head>\n  <body>\n    <div id="div1" style="border: 2px solid black"></div>\n  </body>\n</html>\nuE000\n#module1.js\nimport { divStyle1, divStyle2 } from './module2.js'\ndivStyle1.width = "50px"\nconst div1Style = document.getElementById('div1').style\ndiv1Style.backgroundColor = divStyle1.color\ndiv1Style.height = divStyle2.height\ndiv1Style.width = divStyle1.widthuE000#module2.js\nexport const divStyle1 = {\n  color: 'red',\n  height: '100px',\n  width: '100px',\n}\n\nexport const divStyle2 = {\n  color: 'green',\n  height: '50px',\n}	mcq	\N
137	9	Assuming that the index.html and script.js are kept inside the same directory, then what will be the height of the HTML element having ID 'div1' after 20 seconds, if rendered using a browser?	code	#index.html\n<!DOCTYPE html>\n<html lang="en">\n  <head>\n    <meta charset="UTF-8" />\n    <title>Document</title>\n  </head>\n  <body>\n    <div id="div1" style="background-color: red"></div>\n  </body>\n  <script src="script.js"></script>\n</html>\nuE000\nvar height = 0\nvar width = 0\nvar divStyle = document.getElementById('div1').style\nlet res = setInterval(() => {\n  height += 50\n  width += 50\n  divStyle.height = height + 'px'\n  divStyle.width = width + 'px'\n  console.log(height)\n}, 1000)\nuE000\n#script.js\nsetTimeout(() => {\n  clearInterval(res)\n}, 10050)	mcq	\N
283	37	Note: $C(A),R(A),N(A)$ denote column space, row space and null space of a matrix $A$.\r\n\r\nWhich of the following is/are true about column space of matrix $A$?	text		mcq	\N
284	37	Note: $C(A),R(A),N(A)$ denote column space, row space and null space of a matrix $A$.\r\n\r\nIf $x$ and $y$ belong to the null space of $A$, then the linear combinations of $x$ and $y$ also belong to the null space of $A$.	\N	\N	mcq	\N
285	37	Note: $C(A),R(A),N(A)$ denote column space, row space and null space of a matrix $A$.\r\n\r\nWhich of the following is true about the null space of matrix $A$?	\N	\N	mcq	\N
286	37	Note: $C(A),R(A),N(A)$ denote column space, row space and null space of a matrix $A$.\r\n\r\nA vector $x$ belongs to null space of a matrix $A$ if	\N	\N	mcq	\N
287	37	Gaussian elimination changes the null space of a matrix.	\N	\N	mcq	\N
288	37	Note: $C(A),R(A),N(A)$ denote column space, row space and null space of a matrix $A$.\r\n\r\nIf a $n \\times n$ matrix $A$ is invertible, then which of the following is/are false?	\N	\N	mcq	\N
289	37	Note: $C(A),R(A),N(A)$ denote column space, row space and null space of a matrix $A$.\r\n\r\nWhich of the following is/are true about a $m \\times n$ matrix $A$?	\N	\N	mcq	\N
290	37	Statements regarding the rank of a matrix:\r\n\r\n1. Rank of a matrix is equal to the dimension of its column space.\r\n\r\n2. Rank of a matrix is equal to the dimension of its row space.\r\n\r\n3. Rank of a matrix is equal to the dimension of its null space.\r\n\r\n4. Rank of a matrix is equal to the number of columns of the matrix.\r\n\r\nWhich of the above statements are true?	\N	\N	mcq	\N
291	38	Length of a vector $x$	\N	\N	mcq	\N
292	38	Note: $x.y$ denotes inner product between vectors $x$ and $y$.\r\n\r\nTwo real vectors $x$ and $y$ are orthogonal if:	text		mcq	\N
293	38	Which of the following vectors is orthogonal to any given vector?	\N	\N	mcq	\N
294	38	If two vectors $x_1$ and $x_2$ are orthogonal, then they are not linearly independent.	\N	\N	mcq	\N
295	38	Note: $x.y$ denotes inner product between vectors $x$ and $y$.\r\n\r\nTwo vectors $x$ and $y$ are orthonormal if	\N	\N	mcq	\N
296	38	Two subspaces $S_1$ and $S_2$ are orthogonal if:	text		mcq	\N
297	38	Which of the following is/are true?\r\n\r\n(Note: $\\perp$ denotes orthogonal complement of)	\N	\N	mcq	\N
298	39	A system of equations $Ax=b$ is inconsistent if:	\N	\N	mcq	\N
299	39	The column space of the projection matrix of a vector $v$ is	\N	\N	mcq	\N
300	39	Statements regarding a projection matrix $P$:\r\n\r\n1. $P^2=P$\r\n\r\n2. $P$ is symmetric\r\n\r\n3. $P^2 \\neq P$\r\n\r\n4. $P$ is not symmetric\r\n\r\nWhich of the above statements are true?	\N	\N	mcq	\N
301	39	The null space of the projection matrix of a vector $v$ is	\N	\N	mcq	\N
302	39	The projection matrix $P$ of a vector $a$ is given by:	\N	\N	mcq	\N
303	40	If an $n \\times n$ matrix $A$ is invertible then	\N	\N	mcq	\N
304	40	Consider the projection matrix that projects vectors onto the column space of a matrix $A$ of shape $m \\times n$. Under what conditions does $b \\in \\mathbb{R}^n$ remain unchanged after the projection?	\N	\N	mcq	\N
305	40	Statements regarding the projection matrix $P$:\r\n\r\n1. $P^T=P$\r\n\r\n2. $P^T=-P$\r\n\r\n3. $P^2=P$\r\n\r\n4. $P^2=-P$\r\n\r\nWhich of the above statements are true?	\N	\N	mcq	\N
306	41	If $A\\theta=b$ has a solution then,	\N	\N	mcq	\N
307	41	The least squares solution to a system of linear equations $A\\theta=b$	\N	\N	mcq	\N
308	41	The least squares solution to a system of linear equations $A\\theta=b$	\N	\N	mcq	\N
309	42	What is the length of the vector $\\begin{bmatrix} 1 \\\\ 1 \\\\ -1 \\end{bmatrix}$?	\N	\N	mcq	\N
310	42	The inner product of $\\begin{bmatrix} 1 \\\\ 0 \\\\ 3 \\end{bmatrix}$ and $\\begin{bmatrix} -1 \\\\ 2 \\\\ 4 \\end{bmatrix}$ is	\N	\N	mcq	\N
311	42	The rank of the matrix, $A=\\begin{bmatrix} 0 & 1 & 2 \\\\ 1 & 2 & 7 \\\\ 2 & 1 & 8 \\end{bmatrix}$ is	\N	\N	mcq	\N
312	42	The rank of the matrix, $A=\\begin{bmatrix} 1 & 0 & 2 \\\\ 2 & 1 & 0 \\\\ 3 & 2 & 1 \\end{bmatrix}$ is	\N	\N	mcq	\N
313	42	Can we span the entire 4-d space using the four column vectors given in the following matrix?\r\n\r\n$\\begin{bmatrix} 1 & 2 & 3 & 4 \\\\ 0 & 2 & 2 & 0 \\\\ 1 & 0 & 3 & 0 \\\\ 0 & 1 & 0 & 4 \\end{bmatrix}$	\N	\N	mcq	\N
314	42	What is the rank of the following matrix?\r\n\r\n$\\begin{bmatrix} 2 & 6 & 8 \\\\ 3 & 7 & 10 \\\\ 4 & 8 & 12 \\\\ 5 & 9 & 14 \\end{bmatrix}$	\N	\N	mcq	\N
315	42	The rank of the following matrix $\\begin{bmatrix} 1 & 2 & 3 \\\\ 2 & 3 & 6 \\\\ 4 & 5 & 9 \\end{bmatrix}$ is	\N	\N	mcq	\N
316	42	Rank of a $4 \\times 3$ matrix is 2, what is the dimension of its null space?	\N	\N	mcq	\N
317	42	Which of the following represents the row space of the matrix $\\begin{bmatrix} 2 & 4 & 6 & 8 \\\\ 1 & 3 & 0 & 5 \\\\ 1 & 1 & 6 & 3 \\end{bmatrix}$?\r\n\r\n(Note: $\\text{span } \\{S\\}$ denotes the set of linear combinations of the elements of $S$)	\N	\N	mcq	\N
318	42	Find the projection matrix for $v = \\begin{bmatrix} 3 \\\\ 3 \\\\ 3 \\end{bmatrix}$	\N	\N	mcq	\N
319	42	Find the projection of $\\begin{bmatrix} 1 \\\\ -4 \\\\ 2 \\end{bmatrix}$ along $\\begin{bmatrix} 1 \\\\ -2 \\\\ -3 \\end{bmatrix}$	\N	\N	mcq	\N
320	44	If $P$ is a projection matrix, then the eigenvalue corresponding to every nonzero vector lying in the column space of $P$ is	\N	\N	mcq	\N
321	44	The determinant of a $2 \\times 2$ matrix having eigenvalues 0 and 3 will be	\N	\N	mcq	\N
322	44	The trace of a $2 \\times 2$ matrix A is 4, and its determinant is 3. The eigenvalues of A are	\N	\N	mcq	\N
323	44	If the eigenvalues of a matrix are -1, 3 and 4\r\n\r\nFind the Trace?	\N	\N	numerical	6
324	44	If the eigenvalues of a matrix are -1, 3 and 4\r\n\r\nFind the Determinant?	\N	\N	numerical	-12
325	44	The characteristic polynomial for the matrix $A = \\begin{bmatrix} 1 & 2 \\\\ 2 & 3 \\end{bmatrix}$ is	\N	\N	mcq	\N
326	44	The eigenvalues of the matrix $A = \\begin{bmatrix} 1 & 2 \\\\ 2 & 3 \\end{bmatrix}$ are	\N	\N	mcq	\N
327	44	If matrix $A$ has eigenvalues 1, -2 and 3 then the eigenvalues of $A^2$ are	\N	\N	mcq	\N
328	44	The 90th term of Fibonacci sequence is approximately given by	\N	\N	mcq	\N
329	44	If $x$ is an eigenvector of a matrix $A$, then\r\n\r\n1. $A$ can shrink $x$\r\n\r\n2. $A$ can stretch $x$\r\n\r\n3. $A$ can change the basis of $x$\r\n\r\n4. $A$ does not change the basis of $x$	\N	\N	mcq	\N
330	44	If $A$ is a real symmetric $n \\times n$ matrix, then which of the following is/are true?	\N	\N	mcq	\N
331	44	The eigenvalues of the matrix $\\begin{bmatrix} 1 & 2 \\\\ 4 & 3 \\end{bmatrix}$ are	\N	\N	mcq	\N
332	44	Which of the following are the eigenvectors of matrix $A = \\begin{bmatrix} 1 & 2 \\\\ 3 & 2 \\end{bmatrix}$ ?	\N	\N	mcq	\N
333	44	Statements regarding a given permutation matrix $A$:\r\n\r\n1. 1 is an eigen value of $A$\r\n\r\n2. -1 is an eigen value of $A$\r\n\r\nWhich of the above statements are always true?	\N	\N	mcq	\N
335	45	For a linear regression problem $A\\theta=Y$, with A, Y as in lecture notes, which of the following is the correct equation of the loss function?	\N	\N	mcq	\N
259	36	Execute the the following code-block. Assume that `word1` and `word2` are strings that have already been defined.\r\n\r\nSelect the statement that accurately describes the two lines in the output.	code	#word1, word2 are two strings\nprint(word1 + word2)\nword = word1\nword1 = word2\nword2 = word\nprint(word2 + word1)	mcq	\N
334	44	The best second degree polynomial that fits the data set\n\n| x | y |\n|---|---|\n| 0 | 0 |\n| 1.5 | 1.5 |\n| 4 | 1 |\n\nis	\N		mcq	\N
336	45	For a linear regression problem $A\\theta=Y$, the least squares solution $\\theta=(A^TA)^{-1}A^TY$ exits if	\N	\N	mcq	\N
337	45	Least square regression solves a maximum likelihood estimation problem under a linear model	\N	\N	mcq	\N
338	45	For $\\lambda>0$, $(A^TA+\\lambda I)$ is always invertible	\N	\N	mcq	\N
339	46	If an eigenvalue of a matrix $A$ is zero, then its corresponding eigenvector belongs to	\N	\N	mcq	\N
340	46	For a real symmetric matrix	\N	\N	mcq	\N
341	46	For a matrix $A$ with eigenvalue $\\lambda$, the corresponding eigenvector lies in the	\N	\N	mcq	\N
342	46	$A=aI+B$ where $A$ and $B$ are matrices and $a$ is a scalar. ($I$ is the identity matrix). Which of the following is true?	\N	\N	mcq	\N
343	46	For a matrix $A$ having eigenvalue $\\lambda$, $A-\\lambda I$ is	\N	\N	mcq	\N
344	46	If $x$ is an eigenvector of $A$ corresponding to eigenvalue $\\lambda_1$ and $x$ is also an eigenvector of $B$ corresponding to eigenvalue $\\lambda_2$, then $x$ is also an eigenvector of $(A+B)$.	\N	\N	mcq	\N
345	46	A permutation matrix has eigenvalue(s):	\N	\N	mcq	\N
346	47	All matrices are diagonalizable.	\N	\N	mcq	\N
347	47	If the eigenvalues of a matrix are distinct, then its eigenvectors are linearly independent.	\N	\N	mcq	\N
349	47	If $S^{-1}AS=\\Lambda$, then $S$ is unique.	\N	\N	mcq	\N
348	47	A matrix $A$ satisfies $S^{-1}AS=\\Lambda$ then\n\n1. $S$ contains eigenvectors of $A$\n\n2. $\\Lambda$ contains eigenvalues of $A$\n\nWhich of the above statements is/are true?	\N		mcq	\N
350	47	If $S^{-1}AS=\\Lambda$, then which of the following is true?	\N		mcq	\N
351	48	The eigenvalues of the matrix $A = \\begin{bmatrix} 1 & 1 \\\\ 1 & 0 \\end{bmatrix}$ are:	\N	\N	mcq	\N
352	48	The eigenvectors of $A = \\begin{bmatrix} 1 & 1 \\\\ 1 & 0 \\end{bmatrix}$ are:	\N	\N	mcq	\N
353	49	A matrix $P$ is orthogonal if	\N	\N	mcq	\N
354	49	Suppose that $A$ and $P$ are $2 \\times 2$ matrices and $P$ is invertible matrix.\r\n\r\nIf $P^{-1}AP=\\begin{bmatrix} 2 & 1 \\\\ 0 & 3 \\end{bmatrix}$, then the eigenvalues of the matrix $A$ are	\N	\N	mcq	\N
355	50	The length of the vector $\\begin{bmatrix} 1 \\\\ 2 \\\\ -1 \\end{bmatrix}$ is	\N	\N	mcq	\N
356	50	The inner product of $\\begin{bmatrix} 1 \\\\ 2 \\\\ 3 \\end{bmatrix}$ and $\\begin{bmatrix} -1 \\\\ 1 \\\\ 5 \\end{bmatrix}$ is	\N	\N	mcq	\N
357	50	The rank of a $4 \\times 3$ matrix is 1, what is the dimension of its null space?	\N	\N	mcq	\N
358	50	Which of the following vector is orthogonal to $\\begin{bmatrix} 1 \\\\ -1 \\\\ 3 \\end{bmatrix}$?	\N	\N	mcq	\N
359	50	The rank of the following matrix $\\begin{bmatrix} 1 & 2 & 3 \\\\ 2 & 4 & 6 \\\\ 3 & 6 & 9 \\end{bmatrix}$ is	\N	\N	mcq	\N
360	50	Which of the following would be the smallest subspace containing the first quadrant of the space $\\mathbb{R}^2$?	\N	\N	mcq	\N
361	50	5 peaches and 6 oranges cost 150 rupees. \r\n\r\n10 peaches and 12 oranges cost 300 rupees. \r\n\r\nForm a matrix out of the given information and find its rank.	\N	\N	mcq	\N
362	50	A set of 3 paired observations on $(x_i, b_i), i=1,2,3$ as $((1,6), (-1,3), (3,15))$. \r\n\r\nFor the closest line $b$ to go through these points, which of the following is the least squares solution $(\\hat{\\theta})$?	\N	\N	mcq	\N
363	50	Which of the following represents the null space of the matrix $\\begin{bmatrix} 2 & 4 & 6 & 8 \\\\ 1 & 3 & 0 & 5 \\\\ 1 & 1 & 6 & 3 \\end{bmatrix}$	\N	\N	mcq	\N
364	50	Which of the two vectors are orthogonal to each other?	\N	\N	mcq	\N
365	50	Find projection of $[5, -4, 1]$ along $[3, -2, 4]$	\N	\N	mcq	\N
366	50	The projection matrix for the vector $v = \\begin{bmatrix} 2 \\\\ 1 \\\\ 3 \\end{bmatrix}$ is	\N	\N	mcq	\N
367	50	Find projection of $[2, -4, 4]$ along $[2, -2, 1]$	\N	\N	mcq	\N
368	51	Let $A = \\{-5, -0.5, 5, 3.5, 0.5, 0\\}$. $A$ is a subset of which of the following?	\N	\N	mcq	\N
369	51	Which of the following correctly represent $[a,b]^d$?	\N	\N	mcq	\N
370	51	If the vectors $u$ and $v$ belong to a vector space $V$, then,	\N	\N	mcq	\N
371	51	Which of the following statements are correct as per De Morgan's law?	\N	\N	mcq	\N
372	51	Two vectors $x$ and $y$ are perpendicular to each other if	\N	\N	mcq	\N
373	51	For a real-valued function, which of the following is true?	\N	\N	mcq	\N
374	52	A function is said to be continuous in $\\mathbb{R}$ if:	\N	\N	mcq	\N
375	52	The function $|x|$ is continuous but not differentiable at $x=0$.	\N	\N	mcq	\N
376	52	Choose the correct statement/s from the following:	\N	\N	mcq	\N
377	52	A function $f(x)$ is continuous at a point $x_0$ if	\N	\N	mcq	\N
378	53	Higher order approximations are more accurate than linear approximation.	\N	\N	mcq	\N
379	53	The plot of linear approximation of a function $f$ at a point $v$ is	\N	\N	mcq	\N
380	53	The length of the vector $v=[1,2,3]$ is	\N	\N	numerical	3.73,3.75
381	53	Which of the following vectors is/are perpendicular to any given vector?	\N	\N	mcq	\N
382	54	Which of the following represents a multivariate function?	\N	\N	mcq	\N
383	54	A hyperplane normal to a vector $w$ with offset value $b$ is given by $\\{x:w^Tx=b\\}$.	\N	\N	mcq	\N
384	54	The critical point for the function $f(x)=x^2-x$ is	\N	\N	mcq	\N
385	54	For the function $f(x)=x^2-x$,	\N	\N	mcq	\N
386	55	A line through point $u$ along vector $v$ is given by $\\{x:x=u+\\alpha v\\}$.	\N	\N	mcq	\N
387	55	Gradient of a function evaluated at a point is a vector.	\N	\N	mcq	\N
388	55	Contour plots of linear functions look like	\N	\N	mcq	\N
389	55	The line through $\\begin{bmatrix} 1 \\\\ -1 \\end{bmatrix}$ along $\\begin{bmatrix} 1 \\\\ 3 \\end{bmatrix}$ is given by	\N	\N	mcq	\N
390	56	The statement that the inner product of two complex vectors is always commutative is	\N	\N	mcq	\N
391	56	Which of the following computes the square of the length of $x_1 \\in \\mathbb{R}^n$ and $x_2 \\in \\mathbb{C}^n$ correctly?	\N	\N	mcq	\N
392	56	Given a complex matrix $A$, the notation $A^*$ stands for	\N	\N	mcq	\N
393	56	Properties of conjugate transpose:	\N	\N	mcq	\N
394	56	Properties for complex vectors $x$ and $y$:\r\n(Note: (i) $c$ is a complex number. (ii) $x \\cdot y$ denotes the inner product between vectors $x$ and $y$.)\r\n\r\n1. $x \\cdot y = y \\cdot x$\r\n\r\n2. $x \\cdot y = \\overline{y \\cdot x}$\r\n\r\n3. $x \\cdot (cy) = c(x \\cdot y)$\r\n\r\n4. $(cx) \\cdot y = \\bar{c}(x \\cdot y)$\r\n\r\nWhich of the above properties are correct?	\N	\N	mcq	\N
395	56	The conjugate transpose of $A = \\begin{bmatrix} 1 & 1-i \\\\ 2-3i & 2i \\end{bmatrix}$ is	\N	\N	mcq	\N
396	57	Hermitian matrices in a complex vector space are generalization of	\N	\N	mcq	\N
397	57	Hermitian matrices are orthogonally diagonalizable if their eigenvalues are distinct.	\N	\N	mcq	\N
398	57	The diagonal elements of a Hermitian matrix are real. The statement is	\N	\N	mcq	\N
399	57	The eigenvalues of a Hermitian matrix are	\N	\N	mcq	\N
400	57	The eigenvectors corresponding to distinct eigenvalues of a Hermitian matrix are orthogonal.	\N	\N	mcq	\N
401	57	All real symmetric matrices are Hermitian.	\N	\N	mcq	\N
402	58	A matrix $U$ is unitary if	\N	\N	mcq	\N
403	58	If $U$ is unitary, then which of the following statements are true?	\N	\N	mcq	\N
404	58	The eigenvectors corresponding to distinct eigenvalues of a unitary matrix are	\N	\N	mcq	\N
405	58	Every unitary matrix is a Hermitian matrix.	\N	\N	mcq	\N
406	58	Which of the following is true about an eigenvalue $\\lambda$ of a unitary matrix?	\N	\N	mcq	\N
407	59	For a ________ matrix $A$, we can find a _________ matrix $B$ such that $A=B\\Lambda B^*$ where $\\Lambda$ is a diagonal matrix with eigenvalues of $A$.	\N	\N	mcq	\N
408	59	As per the spectral theorem	\N	\N	mcq	\N
409	60	The Schur's theorem states that	\N	\N	mcq	\N
410	60	For any Hermitian matrix $A$, the spectral theorem states that $D=U^*AU$, where $U$ is a unitary matrix and $D$ is	\N	\N	mcq	\N
411	60	Every unitarily diagonalizable matrix is a Hermitian matrix.	\N	\N	mcq	\N
412	60	Every Hermitian matrix is unitarily diagonalizable.	\N	\N	mcq	\N
413	61	The complex conjugate of matrix $A=\\begin{bmatrix} 1-i & 6+4i \\\\ 1-3i & 35-2i \\end{bmatrix}$ is	\N	\N	mcq	\N
414	61	The complex conjugate transpose of matrix $A=\\begin{bmatrix} 3-2i & 1+4i \\\\ 5+i & 7-2i \\end{bmatrix}$ is	\N	\N	mcq	\N
415	61	The inner product of $x=\\begin{bmatrix} 1-i \\\\ 2i \\end{bmatrix}$ and $y=\\begin{bmatrix} -1-i \\\\ i \\end{bmatrix}$ is	\N	\N	mcq	\N
416	61	The square of the length of vector $x=\\begin{bmatrix} 2-i \\\\ 4-i \\end{bmatrix}$ is	\N	\N	mcq	\N
417	61	The matrix $A=\\begin{bmatrix} \\frac{1+i}{\\sqrt{3}} & \\frac{i}{\\sqrt{3}} \\\\ \\frac{1+i}{\\sqrt{6}} & \\frac{2i}{\\sqrt{6}} \\end{bmatrix}$ is unitary.	\N	\N	mcq	\N
418	61	The matrix $Z=\\begin{bmatrix} 1 & 2 & 3 \\\\ 2 & 4 & 5 \\\\ 3 & 5 & 6 \\end{bmatrix}$ is Hermitian.	\N	\N	mcq	\N
419	61	Which of the following matrices are Hermitian?	\N	\N	mcq	\N
420	61	The eigenvalues of matrix $A=\\begin{bmatrix} 3 & 2+i & 3i \\\\ 2-i & 0 & 1+i \\\\ -3i & 1-i & 0 \\end{bmatrix}$ are	\N	\N	mcq	\N
421	61	The matrix $A=k\\begin{bmatrix} 1+i & 1-i \\\\ 1-i & 1+i \\end{bmatrix}$ is unitary if k is	\N	\N	mcq	\N
422	61	The matrix $A=\\frac{1}{2}\\begin{bmatrix} 1+i & 1-i \\\\ k & i \\end{bmatrix}$ is unitary if k is	\N	\N	mcq	\N
423	61	Let $A=\\begin{bmatrix} 2 & 1-i \\\\ 1+i & 3 \\end{bmatrix}$. If $A$ can be factorized as $A=UDU^*$, with $U$ denoting a unitary matrix, and $D$ denoting a diagonal matrix, then, $U$ and $D$ are	\N	\N	mcq	\N
424	61	Which of the following matrices is/are unitary?	\N	\N	mcq	\N
425	61	Let $U$ and $V$ be two symmetric matrices. Consider the following statements:\r\n\r\n1. $UV$ is symmetric.\r\n\r\n2. $U+V$ is symmetric.\r\n\r\nThen,	\N	\N	mcq	\N
427	62	Which of the following statement(s) is/are correct?	\N	\N	mcq	\N
429	62	Consider the following Vue application with markup index.html and javascript file app.js.\nWhat will be logged on console and rendered on screen (for the mustache expression 'y'), respectively?\n	code	<!-- index.html -->\n<div id="app">y: {{y}}</div>\n<script src="app.js"></script>\nuE000\n// app.js\nconst app = new Vue({\n  el: '#app',\n  data: {\n    x: 0,\n    y: 0,\n  },\n  watch: {\n    x(p, q) {\n      if (p > q && p > 10) {\n        this.y = 1\n      }\n    },\n  },\n})\n\nfor (let i = 0; i < 20; i++) {\n  app.x++\n}	mcq	\N
433	62	What will be rendered by the browser?	code	<!-- index.html -->\n<div id="app">\n  <comp1></comp1>\n</div>\n\n<script src="app.js"></script>\nuE000\n// app.js\nconst comp1 = {\n  template: '<h4> This is {{name}}</h4>',\n  data: function () {\n    return {\n      name: 'component 1',\n    }\n  },\n}\n\nconst app = new Vue({\n  el: '#app',\n  components: {\n    comp1,\n  },\n})	mcq	\N
430	62	Consider the following Vue application with markup index.html and javascript file app.js.\nWhat will be logged on console and rendered on screen (for the mustache expression 'y'), respectively?\n	code	<!-- index.html -->\n<div id="app">y: {{y}}</div>\n<script src="app.js"></script>\nuE000\n// app.js\nconst app = new Vue({\n  el: '#app',\n  data: {\n    x: 20,\n    y: 40,\n  },\n  beforeCreate() {\n    console.log(this.x)\n  },\n})	mcq	\N
431	62	What will be logged on console and rendered on screen respectively?	code	<!-- index.html -->\n<div id="app">y: {{y}}</div>\n<script src="app.js"></script>\nuE000\n// app.js\nconst app = new Vue({\n  el: '#app',\n  data: {\n    x: 20,\n    y: 40,\n  },\n  created() {\n    console.log(this.x)\n  },\n})	mcq	\N
432	62	If your app displays the name of players who play for MI, what are possible directive/data combinations?	code	<!-- index.html -->\n<div id="app">\n  <p directive> data </p>\n</div>\nuE000\n// app.js\nconst players = [\n  { name: 'Rohit Sharma', role: 'Batsman', team: 'MI' },\n  { name: 'Virat Kohli', role: 'Batsman', team: 'RCB' },\n  { name: 'Jaspreet Bumrah', role: 'Bowler', team: 'MI' },\n]\n\nconst app = new Vue({\n  el: '#app',\n  data: {\n    players: players,\n  },\n})	mcq	\N
434	62	What will be rendered by the browser?	code	<!-- index.html -->\n<div id="app">\n  <comp1></comp1>\n</div>\n\n<script src="app.js"></script>\nuE000\n// app.js\nconst comp1 = {\n  template: '<h4> This is {{name}}</h4>',\n  data: {\n    name: 'component 1',\n  },\n}\n\nconst app = new Vue({\n  el: '#app',\n  components: {\n    comp1: comp1,\n  },\n})	mcq	\N
435	62	What will be rendered by the browser?	code	<!-- index.html -->\n<div id="app">\n  <comp-a></comp-a>\n</div>\n\n<script src="app.js"></script>\nuE000\n// app.js\nconst compA = Vue.component('comp-a', {\n  template: `<h4> Hello: {{ message }}</h4>`,\n  data: function () {\n    return {\n      message: 'Welcome to IITM',\n    }\n  },\n})\n\nconst app = new Vue({\n  el: '#app',\n})	mcq	\N
436	63	Consider the following Vue application. \nWhat will be rendered by the browser?	code	<!-- index.html -->\n<div id="app">{{message}}</div>\n<script src="app.js"></script>\nuE000\n// app.js\nconst dataObj = {\n  message: 'Welcome',\n}\n\nconst optObject = {\n  el: '#app',\n  data: dataObj,\n}\n\nconst app = new Vue(optObject)\napp.message = 'Welcome to iitm online degree'	mcq	\N
426	62	Consider the following Vue application. \nSuppose the application adds a “New item” in the list every time you click on the button “Add Item”, what can be the possible definition of the method addItem?	code	<!-- index.html -->\n<div id="app">\n  <ol>\n    <li v-for="item in items">{{item}}</li>\n  </ol>\n  <button @click="addItem">Add Item</button>\n</div>\n\n<script src="app.js"></script>\nuE000\n// app.js\nconst app = new Vue({\n  el: '#app',\n  data: {\n    items: [],\n  },\n  methods: {\n    // add methods here\n  },\n})	mcq	\N
428	62	Consider the following Vue application. \nWhat will be rendered by the browser after 4 seconds?	code	<!-- index.html -->\n<div id="app">\n  <h4>total payable amount is {{totalPayableAmount}}</h4>\n</div>\n\n<script src="app.js"></script>\nuE000\n// app.js\nconst app = new Vue({\n  el: '#app',\n  data: {\n    principal: 0,\n    annualInterestRate: 0,\n    duration: 0,\n    totalPayableAmount: 0,\n  },\n  computed: {\n    simpleInterest() {\n      return (this.principal * this.annualInterestRate * this.duration) / 100\n    },\n  },\n})\n\nappData = [\n  [2000, 10, 2],\n  [3000, 20, 3],\n  [5000, 30, 4],\n]\n\nlet handler = setInterval(() => {\n  data = appData.pop()\n  app.principal = data[0]\n  app.annualInterestRate = data[1]\n  app.duration = data[2]\n  app.totalPayableAmount += app.simpleInterest\n}, 1000)	mcq	\N
465	65	Consider the following Vue application. If the font size increases by 1em on each click, what is the correct definition of objMethods?	code	<div id="app" v-bind:style="{fontSize:fontSize + 'em'}">\r\n  <p>{{message}}</p>\r\n  <button v-on:click="zoom">click me</button>\r\n</div>\r\nuE000\r\n// app.js\r\nconst dataObj = {\r\n  message: 'IITM online',\r\n  fontSize: 2,\r\n}\r\n\r\nconst optObject = {\r\n  el: '#app',\r\n  data: dataObj,\r\n  methods: objMethods,\r\n}\r\n\r\nconst app = new Vue(optObject)	mcq	\N
439	63	Which of the following is true regarding computed properties?	\N	\N	mcq	\N
440	63	Which of the following is correct regarding watchers in Vue?	\N	\N	mcq	\N
443	63	Which of the following is true?	\N	\N	mcq	\N
455	64	If v-if and v-for are used on the same element, which is true?	\N	\N	mcq	\N
456	64	Which of the following is/are true regarding ref attribute in Vue?	\N	\N	mcq	\N
446	64	Consider the following Vue application. \nWhat will be rendered by the browser?	code	<!-- index.html -->\n<div id="app1">\n  <div id="app2">\n    <div id="app3">\n      <p>The message is: {{ message }}</p>\n    </div>\n  </div>\n</div>\n\n<script src="app.js"></script>\nuE000\n// app.js\nconst a = new Vue({\n  el: '#app1',\n  data: {\n    message: 'Kumar',\n  },\n})\n\nconst b = new Vue({\n  el: '#app2',\n  data: {\n    message: 'Rajput',\n  },\n})\n\nconst c = new Vue({\n  el: '#app3',\n  data: {\n    message: 'Abhishek',\n  },\n})	mcq	\N
437	63	Consider the following Vue application. \nIf the app renders "Hello IITM" (in red font color), what is the possible directive for directive mentioned in div with ID app?	code	<!-- index.html -->\n<div id="app">\n  <div directive></div>\n</div>\n\n<script src="app.js"></script>\nuE000\n// app.js\nconst app = new Vue({\n  el: '#app',\n  data: {\n    text: "<p style='color:red'> Hello IITM </p>",\n  },\n})	mcq	\N
438	63	Consider the following Vue application. \nIf the application toggles between dark theme (color:white, background:black) and normal theme (color:black, background:white) on clicking "change theme", what can be the possible definition of toggleTheme?	code	<!-- index.html -->\n<div id="app">\n  <p v-if="dark" v-bind:style="divStyle">{{message}}</p>\n  <p v-else>{{message}}</p>\n  <button @click="toggleTheme">change theme</button>\n</div>\n\n<script src="app.js"></script>\nuE000\n// app.js\nconst app = new Vue({\n  el: '#app',\n  data: {\n    message: 'IITM Online degree',\n    dark: true,\n    divStyle: {\n      backgroundColor: "black",\n      color: "white"\n    }\n  },\n  methods: {\n    toggleTheme() {\n      // fill definition here\n    },\n  },\n})	mcq	\N
442	63	Consider the following Vue application. \nWhat will be rendered by the browser?	code	<!-- index.html -->\n<div id="app">\n  <ol>\n    <comp v-for="message in messages" :message="message"></comp>\n  </ol>\n</div>\n\n<script src="app.js"></script>\nuE000\n// app.js\nconst comp = {\n  template: '<li> {{ message.message }} </li>',\n  props: ['message'],\n}\n\nconst app = new Vue({\n  el: '#app',\n  data: {\n    messages: [\n      { message: 'This is message1' },\n      { message: 'This is message2' },\n      { message: 'This is message3' },\n    ],\n  },\n  components: {\n    comp,\n  },\n})	mcq	\N
441	63	Consider the following Vue application. \nWhat will be rendered by the browser?	code	<!-- index.html -->\n<div id="app">\n  <comp1></comp1>\n</div>\n\n<script src="app.js"></script>\nuE000\n// app.js\nconst comp1 = {\n  template: '<h4> This is {{name}}</h4>',\n  data: {\n    name: 'component 1',\n  },\n}\n\nconst app = new Vue({\n  el: '#app',\n})	mcq	\N
444	64	Which of the following statement(s) is/are false?	\N	\N	mcq	\N
445	64	Which of the following statements is true regarding Vue directives?	\N	\N	mcq	\N
451	64	Consider the following program. \nSuppose isActive = false. What will be rendered?	code	<div class="class1" v-bind:class="{class2:isActive}">	mcq	\N
447	64	Which of the following is/are true regarding computed property in Vue framework?	\N	\N	mcq	\N
448	64	Which of the following is/are true regarding computed properties?	\N	\N	mcq	\N
449	64	Which of the following statement is correct for the Vue framework?	\N	\N	mcq	\N
450	64	Consider the following program. Suppose isActive = true. What will be rendered?	code	<div class="class1" v-bind:class="{class2:isActive}">	mcq	\N
454	64	Which of the following is true?	\N	\N	mcq	\N
452	64	What will be the color and font-weight of "hello world"?	code	<!-- index.html -->\n<body>\n  <div\n    id="app"\n    v-bind:style="[style1, style2]"\n  >\n    hello world\n  </div>\n</body>\n\n<script src="app.js"></script>\nuE000\n// app.js\nconst style1 = {\n  color: 'red',\n}\n\nconst style2 = {\n  fontWeight: 'bold',\n}\n\nconst optObject = {\n  el: '#app',\n  data: { style1: style1, style2: style2 },\n}\n\nconst app = new Vue(optObject)	mcq	\N
453	64	What will be the color and font-weight of "hello world"?	code	<!-- index.html -->\n<body>\n  <div\n    id="app"\n    v-bind:style="[style1]"\n  >\n    hello world\n  </div>\n</body>\n\n<script src="app.js"></script>\nuE000\n// app.js\nconst style1 = {\n  color: 'red',\n}\n\nconst style2 = {\n  fontWeight: 'bold',\n}\n\nconst optObject = {\n  el: '#app',\n}	mcq	\N
457	65	Which of the following is/are examples of system level state that needs to be maintained for the entire app?	\N	\N	mcq	\N
458	65	Which of the following could be considered user specific application state?	\N	\N	mcq	\N
459	65	When you view the online discourse forum, there is a line indicating “last visit” - posts above this have been updated since the last time you visited the forum. What kind of state information is this indicator conveying?	\N	\N	mcq	\N
460	65	Which of the following methods can be used to ensure that the displayed state and system state are kept in sync at all times?	\N	\N	mcq	\N
461	65	The M in MVC stores ____.	\N	\N	mcq	\N
462	65	Consider the following Vue application. What will be rendered by the browser?	code	<div id="app">{{newMessage}}</div>\r\nuE000\r\n// app.js\r\nconst dataObj = {\r\n  message: 'Welcome',\r\n}\r\n\r\nconst optObject = {\r\n  el: '#app',\r\n  data: dataObj,\r\n}\r\n\r\nconst app = new Vue(optObject)\r\napp.newMessage = 'Welcome to iitm online degree'	mcq	\N
463	65	Consider the following Vue application. What will be rendered by the browser after 1 minute?	code	<div id="app">{{count + ' second remaining'}}</div>\r\nuE000\r\n// app.js\r\nconst dataObj = {\r\n  count: 10000,\r\n}\r\n\r\nconst optObject = {\r\n  el: '#app',\r\n  data: dataObj,\r\n}\r\n\r\nconst app = new Vue(optObject)\r\n\r\nsetInterval(() => {\r\n  app.count -= 1\r\n}, 1000)	mcq	\N
464	65	Consider the following Vue application. What will be the color, background color and font-size of the div with ID "app"?	code	<div id="app" style="color: white" v-bind:style="divStyle">{{message}}</div>\r\nuE000\r\n// app.js\r\nconst dataObj = {\r\n  message: 'IITM online',\r\n  divStyle: {\r\n    backgroundColor: 'red',\r\n    padding: '20px',\r\n    fontSize: '2em',\r\n  },\r\n}\r\n\r\nconst optObject = {\r\n  el: '#app',\r\n  data: dataObj,\r\n}\r\n\r\nconst app = new Vue(optObject)	mcq	\N
466	65	Consider the following Vue application. If you want to toggle the presence of the <p> element when the button is clicked, what should directive1 and directive2 be?	code	<div id="app">\r\n  <p directive1>{{message}}</p>\r\n  <button directive2>click</button>\r\n</div>\r\nuE000\r\n// app.js\r\nconst app = new Vue({\r\n  el: '#app',\r\n  data: {\r\n    message: 'Hello',\r\n    seen: true,\r\n  },\r\n  methods: {\r\n    toggleSeen() {\r\n      this.seen = !this.seen\r\n    },\r\n  },\r\n})	mcq	\N
467	66	If an application is entirely built on the client end using JavaScript (without database). Which of the following statements is true?	\N	\N	mcq	\N
468	66	Which of the following statement(s) is/are correct?	\N	\N	mcq	\N
469	66	Which of the following is a desirable trait for good UI design?	\N	\N	mcq	\N
470	66	Which of the following statement(s) is/are true?	\N	\N	mcq	\N
471	66	Which of the following is correct regarding application state?	\N	\N	mcq	\N
472	66	All news article published on The Hindu newspaper is an example of ____.	\N	\N	mcq	\N
473	67	Which of the following is/are example(s) of persistent state/data?	\N	\N	mcq	\N
474	67	What is UX(User Experience) design?	\N	\N	mcq	\N
475	67	What is UI design?	\N	\N	mcq	\N
476	67	Which of the following is correct regarding ephemeral state?	\N	\N	mcq	\N
477	67	Aesthetics of a page in web design comes under the ___.	\N	\N	mcq	\N
478	67	Entire database of Flipkart comes under ____.	\N	\N	mcq	\N
479	67	How user will interact with the Spotify playlist comes under ___?	\N	\N	mcq	\N
480	68	Consider the following JavaScript program. Which of the following shows the correct output if the program is executed?	code	// program.js\r\nclass A {\r\n\r\n  constructor(name){\r\n    this.name = name;\r\n  }\r\n\r\n}\r\n\r\nobj = new A("Abhi");\r\nconsole.log(typeof(JSON.stringify(obj)));	mcq	\N
481	68	Consider the following JavaScript program. Which of the following shows the correct output if the program is executed?	code	// program.js\r\nclass A {\r\n\r\n  constructor(name){\r\n    this.name = name;\r\n  }\r\n\r\n}\r\n\r\nobj = new A("Abhi");\r\ntemp = JSON.stringify(obj);\r\nconsole.log(typeof(JSON.parse(temp)));	mcq	\N
482	69	Consider the following JavaScript program. What will be the output of the following program?	code	// program.js\r\nx = [1, 2, 3, 4, 5, 6]\r\n\r\nv = x.reduce((a, i) => a + i, 10)\r\n\r\nconsole.log(v)	mcq	\N
483	69	What is run-to-completion semantics in the context of JavaScript?	\N	\N	mcq	\N
484	70	Consider the following JavaScript program. Which of the following shows the correct output?	code	// program.js\r\nlet a = { 'a': 1, 'b': 2, 'c': function() { return "Hello"; } }\r\n\r\nlet b = { __proto__: a, 'd': 3 }\r\n\r\nconsole.log(b.b, b.c())	mcq	\N
485	70	Consider the following JavaScript program. Which of the following shows the correct output?	code	// program.js\r\nclass A {\r\n\r\n  constructor(name) {\r\n    this.name = name;\r\n  }\r\n\r\n  get output() {\r\n    return this.name;\r\n  }\r\n\r\n  set input(name) {\r\n    this.name = name;\r\n  }\r\n\r\n}\r\n\r\nobj = new A();\r\nobj.input = "Abhi";\r\n\r\nconsole.log(obj.output);	mcq	\N
486	70	Consider the following JavaScript program. What will be the output?	code	// program.js\r\nx = [1, 2, 3, 4, 5, 6]\r\n\r\ny = [...x, 7, 8, 9]\r\n\r\nconsole.log(y.length)	mcq	\N
487	70	Consider the following JavaScript program. What will be the output?	code	// program.js\r\nx = [1, 2, 2, 4, 5, -2, -7, -9]\r\n\r\nconsole.log(x.sort((a, b) => a - b))	mcq	\N
488	70	Consider the following JavaScript program. What will be the output?	code	// program.js\r\nx = [1, 2, 2, 4, 5, -2, -7, -9]\r\n\r\nconsole.log(x.sort((a, b) => b - a))	mcq	\N
489	71	Consider the following JavaScript program. Which of the following shows the correct output?	code	// program.js\r\nfunction func(x) { \r\n  return x % 2; \r\n}\r\n\r\nlet a = [5, 15, 25, 35, 45];\r\n\r\nconsole.log(a.map(func));	mcq	\N
490	71	Consider the following JavaScript program. Which of the following shows the correct output?	code	// program.js\r\na = [1, 2, 3];\r\n[b, c] = a;\r\n\r\nconsole.log(c);	mcq	\N
491	71	Consider the following JavaScript program. Which of the following shows the correct output?	code	// program.js\r\na = [1, 2, 3];\r\nb, c = a;\r\n\r\nconsole.log(c);	mcq	\N
492	71	Consider the following JavaScript program. Which of the following shows the correct output?	code	// program.js\r\na = [1, 2, 3];\r\n[b, ...c] = a;\r\n\r\nconsole.log(c);	mcq	\N
493	71	Consider the following JavaScript program. What will be the output?	code	// program.js\r\nx = new Array(5)\r\n\r\nx[0] = 1\r\nx[1] = 3\r\n\r\ny = []\r\n\r\nfor (i in x) {\r\n  y.push(i)\r\n}\r\n\r\nconsole.log(y.length)	mcq	\N
494	72	What will be the output of the following JavaScript program?	code	let a = [1, 2, 3, 4, 5];\r\nconsole.log(Object.keys(a));	mcq	\N
495	72	What will be the output of the following JavaScript program?	code	let a = [1, 2, 3, 4, 5];\r\nconsole.log(Object.values(a));	mcq	\N
496	72	What will be the output of the following JavaScript program?	code	let a = [1, 2, 3];\r\nconsole.log(Object.entries(a));	mcq	\N
497	72	Which of the following is the correct length of the array 'a', after the execution of the program written below?	code	let a = [1, 2, 3, 4, 5];\r\na.length = 9;	mcq	\N
498	72	Predict the number of holes in the array 'a', after the execution of the program written below?	code	let a = [1, 2, 3, 4, 5];\r\na.length = 9;	mcq	\N
499	72	Which of the following shows the correct output, if the program written below is executed?	code	let a = [2, 3, 4];\r\nlet b = [1, 2, ...a, 5];\r\nconsole.log(b);	mcq	\N
500	73	Which of the following is correct regarding JavaScript array?	\N	\N	mcq	\N
501	73	Which of the following is correct statement.	\N	\N	mcq	\N
502	73	What is a callback function?	\N	\N	mcq	\N
503	73	Which of the following is an iterable object?	\N	\N	mcq	\N
504	73	Which of the following is not a collection?	\N	\N	mcq	\N
505	74	Consider two non-zero vectors $x \\in \\mathbb{C}^n$ and $y \\in \\mathbb{C}^n$. Suppose the inner product between $x$ and $y$ obeys commutative property (i.e., $x \\cdot y = y \\cdot x$). Then	\N	\N	mcq	\N
506	74	The inner product of two distinct vectors $x$ and $y$ that are from $\\mathbb{C}^{100}$ is $0.8 - 0.37i$. The vector $x$ is scaled by a scalar $1 - 2i$ to obtain a new vector $z$, then the inner product between $z$ and $y$ is	\N	\N	mcq	\N
507	74	Select the correct statement(s). The Eigenvalue decomposition for the matrix $A = \\begin{bmatrix} 0 & -1 \\\\ 1 & 0 \\end{bmatrix}$	\N	\N	mcq	\N
508	74	The matrix $S = \\begin{bmatrix} 1 & 1+i & -2-2i \\\\ 1-i & 1 & -i \\\\ -2+2i & i & 1 \\end{bmatrix}$ is	\N	\N	mcq	\N
509	74	Suppose that an unitary matrix $U$ is multiplied by a diagonal matrix $D$ with diagonal elements in $D$ denoted as $d_{ii} \\in \\mathbb{R}$, then the resultant matrix will always be unitary. The statement is	\N	\N	mcq	\N
510	74	The eigenvectors of matrix $A = \\begin{bmatrix} 3 & 2+i & 3i \\\\ 2-i & 0 & 1+i \\\\ -3i & 1-i & 0 \\end{bmatrix}$ are	\N	\N	mcq	\N
511	74	The matrix $A = \\frac{1}{2} \\begin{bmatrix} k+i & \\sqrt{2} \\\\ k-i & i\\sqrt{2} \\end{bmatrix}$ is unitary if k is	\N	\N	mcq	\N
512	74	Let $A = \\begin{bmatrix} 1 & 1-i \\\\ 1+i & 1 \\end{bmatrix}$. If $A$ can be factorized as $A = UDU^*$, with $U$ denoting a unitary matrix and $D$ denoting a diagonal matrix. Then, $U$ and $D$ are	\N	\N	mcq	\N
513	74	The matrix $Z = \\begin{bmatrix} 0 & 0 & 0 & 1 \\\\ 0 & 0 & 1 & 0 \\\\ 0 & 1 & 0 & 0 \\\\ -1 & 0 & 0 & 0 \\end{bmatrix}$ has	\N	\N	mcq	\N
514	74	Which of the following matrices is/are unitary?	\N	\N	mcq	\N
515	74	Let $U$ and $V$ be two unitary matrices. Then,\r\n\r\n1. $UV$ is always unitary.\r\n\r\n2. $U+V$ is always unitary.	\N	\N	mcq	\N
516	74	Which of the following is/are eigenvectors of the matrix $A = \\begin{bmatrix} 1 & 1+i \\\\ 1-i & 2 \\end{bmatrix}$	\N	\N	mcq	\N
517	75	Every matrix can be diagonalized.	\N	\N	mcq	\N
518	75	Every real matrix can be factored using SVD.	\N	\N	mcq	\N
519	75	If an $m \\times n$ matrix $A$ is decomposed as $A=Q_1\\Sigma Q_2^T$ where $Q_1$ and $Q_2$ are orthogonal and $\\Sigma$ is a diagonal matrix then the dimensions of $Q_1$, $Q_2$ and $\\Sigma$ are	\N	\N	mcq	\N
520	75	The singular values of a matrix $A$ are (Mark all the correct options)	\N	\N	mcq	\N
521	75	If $A=Q_1\\Sigma Q_2^T$, then $AA^T$ is	\N	\N	mcq	\N
522	75	If $A=Q_1\\Sigma Q_2^T$, then $A^TA$ is	\N	\N	mcq	\N
523	75	Which of the following statements about matrix decomposition is/are true?\r\n1. Eigendecomposition exists only for real symmetric matrix\r\n2. Any matrix can be factored using Singular Value Decomposition	\N	\N	mcq	\N
\.


--
-- Data for Name: subjects; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.subjects (id, name) FROM stdin;
1	MAD 2
2	JAVA
3	MAD 1
4	DBMS
5	PDSA
6	MLT
7	MLF
8	PYTHON
9	MATHS 2
10	STATS 2
\.


--
-- Data for Name: video_cache; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.video_cache (video_id, ai_data, updated_at) FROM stdin;
\.


--
-- Data for Name: weeks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.weeks (id, subject_id, week_number, youtube_urls) FROM stdin;
5	8	1	\N
8	8	2	\N
9	1	2	\N
10	1	1	\N
7	7	1	{https://www.youtube.com/watch?v=zuS1WZQGhAs&list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN&index=1,https://www.youtube.com/watch?v=zssr9nOZlVg&list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN&index=2,https://www.youtube.com/watch?v=iVcrCdEaJ7A&list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN&index=3,https://www.youtube.com/watch?v=QtOrjs0Fzzc&list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN&index=4,https://www.youtube.com/watch?v=EuNPsw9zA1k&list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN&index=5&t=5s&pp=iAQB,https://www.youtube.com/watch?v=Gj6-61UDeMs&list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN&index=6&pp=iAQB,https://www.youtube.com/watch?v=5G4klfCCoIs,https://www.youtube.com/watch?v=T7vdFVC6DOo,https://www.youtube.com/watch?v=JG5Z9np4Tbs}
1	7	2	{https://www.youtube.com/watch?v=Gi9nUcrZAJs&list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN&index=7&pp=iAQB0gcJCa4KAYcqIYzv,https://www.youtube.com/watch?v=yvaPORg2w9c&list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN&index=8&pp=iAQB,https://www.youtube.com/watch?v=AG2fQvxEpbE&list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN&index=9&pp=iAQB,https://www.youtube.com/watch?v=En15LA59Fsw&list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN&index=10&pp=iAQB0gcJCa4KAYcqIYzv,https://www.youtube.com/watch?v=O5jrvVi05wA&list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN&index=11&pp=iAQB,https://www.youtube.com/watch?v=dLLbl0vucCc&list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN&index=12&pp=iAQB,https://www.youtube.com/watch?v=YNJMUyNlqFQ}
11	2	1	\N
4	7	3	{https://www.youtube.com/watch?v=9Ynm5oJRjxY&list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN&index=13&pp=iAQB,https://www.youtube.com/watch?v=pDVywF7yLaM&list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN&index=14&pp=iAQB,https://www.youtube.com/watch?v=kVYR7II5KUA&list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN&index=15&pp=iAQB,https://www.youtube.com/watch?v=_QRlIQBwIk8&list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN&index=16&pp=iAQB0gcJCa4KAYcqIYzv,https://www.youtube.com/watch?v=wZlwod57blE&list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN&index=17&pp=iAQB0gcJCa4KAYcqIYzv,https://www.youtube.com/watch?v=rbBiDiFC584,https://www.youtube.com/watch?v=kRJIiQXiOqU,https://www.youtube.com/watch?v=Ijn-HGlVifU,https://www.youtube.com/watch?v=Mu5Cf9eD4SQ}
2	6	1	{https://www.youtube.com/watch?v=KMcUe7GQnf0&list=PLZ2ps__7DhBbA_e6_G3FI-BA1f7lCINUu&index=1&pp=iAQB,https://www.youtube.com/watch?v=ipjggYk7zXs&list=PLZ2ps__7DhBbA_e6_G3FI-BA1f7lCINUu&index=2&pp=iAQB,https://www.youtube.com/watch?v=1V_M4JxygGk&list=PLZ2ps__7DhBbA_e6_G3FI-BA1f7lCINUu&index=3&pp=iAQB,https://www.youtube.com/watch?v=mU6CzvuUM00&list=PLZ2ps__7DhBbA_e6_G3FI-BA1f7lCINUu&index=4&pp=iAQB,https://www.youtube.com/watch?v=t0bA3rsZ6qM&list=PLZ2ps__7DhBbA_e6_G3FI-BA1f7lCINUu&index=5&pp=iAQB,https://www.youtube.com/watch?v=_GOADM-SdKU&list=PLZ2ps__7DhBbA_e6_G3FI-BA1f7lCINUu&index=6&pp=iAQB,https://www.youtube.com/watch?v=o__dWBLqPhQ&list=PLZ2ps__7DhBbA_e6_G3FI-BA1f7lCINUu&index=7&pp=iAQB,https://www.youtube.com/watch?v=BkesMPmhh_E}
13	7	4	{https://www.youtube.com/watch?v=Mu5Cf9eD4SQ,https://www.youtube.com/watch?v=GA6m_T4d_d0&list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN&index=19,https://www.youtube.com/watch?v=WKZUxnrLmRk&list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN&index=20,https://www.youtube.com/watch?v=ISB87lDKOVE&list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN&index=21,https://www.youtube.com/watch?v=f0hVL9xhL94&list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN&index=21&pp=iAQB,https://www.youtube.com/watch?v=EF85-fHy-m0,https://www.youtube.com/watch?v=SPF2ovt7uYg}
3	6	2	{https://www.youtube.com/watch?v=sgU4zbO-W4M&list=PLZ2ps__7DhBbA_e6_G3FI-BA1f7lCINUu&index=8&pp=iAQB,https://www.youtube.com/watch?v=pwpDf2_Pytk&list=PLZ2ps__7DhBbA_e6_G3FI-BA1f7lCINUu&index=9&pp=iAQB,https://www.youtube.com/watch?v=zcxnCyVSh70&list=PLZ2ps__7DhBbA_e6_G3FI-BA1f7lCINUu&index=10&pp=iAQB,https://www.youtube.com/watch?v=K46tdjqxM0w&list=PLZ2ps__7DhBbA_e6_G3FI-BA1f7lCINUu&index=11&pp=iAQB,https://www.youtube.com/watch?v=G6rMGLhw3IQ&list=PLZ2ps__7DhBbA_e6_G3FI-BA1f7lCINUu&index=12&pp=iAQB,https://www.youtube.com/watch?v=Qs8dVQzu43I}
6	6	3	{https://www.youtube.com/watch?v=A3UNtCuMm7Y&list=PLZ2ps__7DhBbA_e6_G3FI-BA1f7lCINUu&index=13&pp=iAQB,https://www.youtube.com/watch?v=QrXQ5cMzphA&list=PLZ2ps__7DhBbA_e6_G3FI-BA1f7lCINUu&index=14&pp=iAQB,https://www.youtube.com/watch?v=5geXmawaImk&list=PLZ2ps__7DhBbA_e6_G3FI-BA1f7lCINUu&index=15&pp=iAQB,https://www.youtube.com/watch?v=EY03QHaaSBY&list=PLZ2ps__7DhBbA_e6_G3FI-BA1f7lCINUu&index=16&pp=iAQB,https://www.youtube.com/watch?v=Cbrdtxq6bdk&list=PLZ2ps__7DhBbA_e6_G3FI-BA1f7lCINUu&index=17&pp=iAQB,https://www.youtube.com/watch?v=4-ycWgdMXD4&list=PLZ2ps__7DhBbA_e6_G3FI-BA1f7lCINUu&index=18&pp=iAQB0gcJCb4KAYcqIYzv,https://www.youtube.com/watch?v=_4mnXtczNoc}
12	6	4	{https://www.youtube.com/watch?v=382yNz5LoX0&list=PLZ2ps__7DhBbA_e6_G3FI-BA1f7lCINUu&index=19&pp=iAQB,https://www.youtube.com/watch?v=9dQSEn0ooTc&list=PLZ2ps__7DhBbA_e6_G3FI-BA1f7lCINUu&index=20&pp=iAQB,https://www.youtube.com/watch?v=ZnkRbtZLPm4&list=PLZ2ps__7DhBbA_e6_G3FI-BA1f7lCINUu&index=21&pp=iAQB,https://www.youtube.com/watch?v=dyRTVmtML-U&list=PLZ2ps__7DhBbA_e6_G3FI-BA1f7lCINUu&index=22&pp=iAQB,https://www.youtube.com/watch?v=a-VVrP11ZIo&list=PLZ2ps__7DhBbA_e6_G3FI-BA1f7lCINUu&index=23&pp=iAQB,https://www.youtube.com/watch?v=4s0aNldT02Y&list=PLZ2ps__7DhBbA_e6_G3FI-BA1f7lCINUu&index=24&pp=iAQB,https://www.youtube.com/watch?v=idWmaE39OIk&list=PLZ2ps__7DhBbA_e6_G3FI-BA1f7lCINUu&index=25&pp=iAQB,https://www.youtube.com/watch?v=1jSonYih_sM&list=PLZ2ps__7DhBbA_e6_G3FI-BA1f7lCINUu&index=26&pp=iAQB,https://www.youtube.com/watch?v=iC215XRWABA}
14	7	5	{https://www.youtube.com/watch?v=G6A3PDivChQ&list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN&index=26,https://www.youtube.com/watch?v=aHykfDdjDiw&list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN&index=26&pp=iAQB,https://www.youtube.com/watch?v=2DAG0I1NKiI&list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN&index=27&pp=iAQB,https://www.youtube.com/watch?v=qG1tlEa2Zn0&list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN&index=28&pp=iAQB,https://www.youtube.com/watch?v=u9uFJNrCL0E&list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN&index=29&pp=iAQB0gcJCa4KAYcqIYzv,https://www.youtube.com/watch?v=__TUd8Sq-wU}
\.


--
-- Name: assessments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.assessments_id_seq', 80, true);


--
-- Name: options_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.options_id_seq', 2003, true);


--
-- Name: questions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.questions_id_seq', 566, true);


--
-- Name: subjects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.subjects_id_seq', 10, true);


--
-- Name: weeks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.weeks_id_seq', 14, true);


--
-- Name: assessments assessments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assessments
    ADD CONSTRAINT assessments_pkey PRIMARY KEY (id);


--
-- Name: mcq_cache mcq_cache_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mcq_cache
    ADD CONSTRAINT mcq_cache_pkey PRIMARY KEY (cache_key);


--
-- Name: options options_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.options
    ADD CONSTRAINT options_pkey PRIMARY KEY (id);


--
-- Name: questions questions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_pkey PRIMARY KEY (id);


--
-- Name: subjects subjects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subjects
    ADD CONSTRAINT subjects_pkey PRIMARY KEY (id);


--
-- Name: video_cache video_cache_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.video_cache
    ADD CONSTRAINT video_cache_pkey PRIMARY KEY (video_id);


--
-- Name: weeks weeks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.weeks
    ADD CONSTRAINT weeks_pkey PRIMARY KEY (id);


--
-- Name: weeks weeks_subject_id_week_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.weeks
    ADD CONSTRAINT weeks_subject_id_week_number_key UNIQUE (subject_id, week_number);


--
-- Name: assessments assessments_subject_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assessments
    ADD CONSTRAINT assessments_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES public.subjects(id);


--
-- Name: options options_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.options
    ADD CONSTRAINT options_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.questions(id);


--
-- Name: questions questions_assessment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_assessment_id_fkey FOREIGN KEY (assessment_id) REFERENCES public.assessments(id);


--
-- Name: weeks weeks_subject_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.weeks
    ADD CONSTRAINT weeks_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES public.subjects(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict 1qvjUFRnOoAmLRlx1l4qRrPbfkdwyr89AfN5zgj5DU6uSk5odANbqVrWuL7zRRQ

