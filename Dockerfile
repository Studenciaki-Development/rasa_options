# Extend the official Rasa SDK image
FROM rasa/rasa-sdk:1.10.2

# Use subdirectory as working directory
WORKDIR /app

# Copy any additional custom requirements, if necessary (uncomment next line)
COPY actions/requirements-actions.txt ./

# Change back to root user to install dependencies
USER root

# Install extra requirements for actions code, if necessary (uncomment next line)
RUN pip install -r requirements-actions.txt

# Copy actions folder to working directory
COPY ./actions /app/actions
COPY ./data /app/data

RUN  rasa train -c ./config.yml -d ./domain.yml --data ./data --debug

EXPOSE 5005
# By best practices, don't run the code with root user
USER 1001

# Start the action server
# CMD ["start", "--actions", "actions.actions"]
VOLUME /app
VOLUME /app/data
VOLUME /app/models
CMD [ "run","-m","/app/models","--enable-api","--cors","*","--debug" ]
