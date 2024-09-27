# Step 3

## Making our first endpoint

### First, we define the "feature"

Requirements:

    - The endpoint should be "/home"
    - A GET request to the endpoint should return a JSON

### Second, we write a test

1. Let's add a test configuration to `configs.py`

    ```python
    class Testing(Default):
        TESTING = True
        DATABASE = os.environ["TEST_DB"]
    ```

    - Note: We don't turn debug mode ON because it doesn't work with Pytest. This makes debugging failed tests a little more cumbersome, but the TESTING flag helps a little

2. You might have noticed I referenced a new environment variable we need to create. Make TEST_DB whatever you want, but I use `TEST_DB='${PWD}/dbs/test.db'`

3. Create tests/conftest.py and write a test fixture that:

    - creates 
