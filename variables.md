# Study Portal Codebase Cheat Sheet

## 1. Functions & Their Roles
These are the reusable blocks of code defined at the top of your file.

* `ask_ai_tutor(...)`: Takes the question context and the user's answer, constructs a prompt, and calls the Gemini API to return a detailed pedagogical explanation.
* `get_db_connection()`: Establishes a connection to your PostgreSQL database. Uses `@st.cache_resource` so it doesn't reconnect on every button click.
* `fetch_data(query, params)`: Executes a `SELECT` SQL query and returns the rows as a list of Python dictionaries.
* `execute_query(query, params)`: Used for `INSERT`, `UPDATE`, or `DELETE` commands. It executes the query and commits the changes to the database.
* `render_content(media_type, content)`: Looks at a question's `media_type` and renders it accordingly (markdown string, Python code block, or an image from the `pic/` folder).
* `render_option_card(label, content, media_type)`: Similar to `render_content`, but wraps the content in an `st.info` box with a styled label (like "OPTION 1").
* `check_numerical_answer(user_val, correct_key)`: Validates numerical inputs, handling precise floats (with a 0.001 tolerance) and range-based answers (e.g., "65,66").

---

## 2. Variables Grouped by Code Snippets

### A. Global / Setup Block
* `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASS`: Database connection credentials.
* `app_mode`: The main navigation state driven by `st.sidebar.radio` (determines if the user sees "Take Assessment", "Take Test", or "Edit Content").

### B. Take Assessment (Study Mode Loop)
* `c1, c2, c3, c4`: Streamlit column layout objects for the top filter dropdowns.
* `subjects`, `s_map`, `s_sel`: Fetches subjects, maps names to IDs, and stores the user's dropdown selection.
* `weeks`, `w_sel` / `assessments`, `a_map`, `a_sel`: Stores fetched data and selections for Weeks and Activities.
* `mode`: Stores the choice between "Study Mode", "Exam Mode", or "AI Tutor Mode".
* `questions`: List of dictionaries containing the questions for the selected assessment.
* `q`: Iterator variable representing the current question dictionary in the loop.
* `val`: Stores the string input from the user for numerical questions.
* `options`: List of dictionaries containing the options for the current `q`.
* `c_disp, c_sel`: Column objects splitting the UI into Option Display (90%) and Select Controls (10%).
* `is_multi`: Boolean checking if the question has multiple correct answers (MSQ).
* `sel_idxs`: List storing the index numbers of checkboxes the user has ticked.
* `choice`: Stores the user's selection from a Radio button (for single-answer MCQs).
* `explanation`: Stores the string response returned from the `ask_ai_tutor` function.

### C. Take Test (Exam Engine)
* `st.session_state.test_state`: Tracks where the user is in the exam flow (`setup`, `running`, or `results`).
* `w_filter`, `t_filter`: SQL-formatted strings used to query multiple selected weeks/activity types at once.
* `num_q`: Stores the number of questions the user wants to attempt.
* `st.session_state.test_data`: A cached list holding tuples of `(question, options)` so the test doesn't re-query the DB.
* `st.session_state.responses`: A dictionary mapping question IDs to the user's provided answers.
* `score`, `total`: Integers calculating the final grade.
* `results_data`: A list formatting the history of the test to display on the final results screen.
* `duration`, `mins`, `secs`: Math variables calculating how long the test took.

### D. Edit Content (Admin CMS)
* `q_map`, `q_sel`, `q_id`: Maps question text to IDs to allow the user to select which question to edit.
* `q_data`, `opts_data`: Holds the current database information to pre-fill the edit form.
* `n_head`, `n_mtype`, `n_cont`, `n_ans`: New values input by the user for Heading, Media Type, Media Content, and Numerical Answer.
* `upd_opts`: A temporary list holding the edited states of all the options before saving.
* `nt`, `nv`, `nc`: Stand for "New Type", "New Value", and "New Correct flag" for an individual option.

---

## 3. CSS Elements Breakdown

* `[data-testid="stAppViewContainer"] [data-testid="stImage"] img`: Restricts inline image sizes to a `max-height` of 300px so questions don't take up too much vertical space.
* `div[data-testid="stFullScreenFrame"] img`: Targets the modal that appears when you expand an image, forcing it to use 95% of the viewport height/width.
* `div[data-testid="stModal"]`: Forces the dark overlay background of the full-screen image viewer to stretch 100% across the screen.
* `.stApp`: Changes the global font family of the entire application to 'Segoe UI'.
* `.block-container`: Adjusts Streamlit's default margins, pulling the content higher up and making it wider.
* `.option-label`: Makes specific texts (like "SELECT") small, uppercase, bold, and gray.
* `.scroll-btn`: Styles the floating "Scroll to top" arrow (fixed position, circular shape, blue background).
* `.scroll-btn:hover`: Adds CSS transitions so the scroll button slightly enlarges and drops a shadow when hovered.
* `button[kind="primary"]`: Overrides Streamlit's default primary button color with your custom blue.
* `footer`: Sets `visibility: hidden;` to remove the default "Made with Streamlit" watermark.

---

## 4. Python Keywords Explained

* `import` / `from`: Used to bring external libraries (like `streamlit`, `psycopg2`) into your script.
* `def`: Short for "define". Used to create a new custom function.
* `if` / `elif` / `else`: Conditional statements controlling the flow of the program based on logic.
* `try` / `except`: Error handling. If code inside `try` crashes, the script jumps to `except` to handle the error gracefully without shutting down the app.
* `return`: Exits a function and passes a value back to whoever called it.
* `None`: A special data type representing the absence of a value or a null value.
* `with`: A context manager. Ensures resources (like database connections) are properly opened and closed automatically.
* `for` / `in`: Creates a loop that iterates over a sequence (like a list of questions).
* `and` / `not` / `or`: Logical operators used to combine or negate conditions.
* `True` / `False`: Boolean values representing binary states (on or off).
* `pass`: A placeholder that does nothing, used when a statement is required syntactically but no code needs to be executed.