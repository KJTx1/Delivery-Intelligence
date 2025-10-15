FROM fnproject/python:3.11 as build-stage
WORKDIR /function

COPY requirements.txt .
RUN python3 -m venv venv && \
    venv/bin/pip install --upgrade pip && \
    venv/bin/pip install --no-cache-dir -r requirements.txt && \
    rm -rf ~/.cache/pip /tmp*

COPY . .

FROM fnproject/python:3.11
WORKDIR /function

COPY --from=build-stage /function/venv venv
COPY --from=build-stage /function .

ENV PYTHONPATH=/function
ENV PATH="/function/venv/bin:$PATH"

ENTRYPOINT ["/function/venv/bin/fdk", "/function/func.py", "handler"]
