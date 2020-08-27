## base + field_of_study 1
* greet
  - utter_greet
  - action_general_options
* field_of_study_limits{"field-of-study":"informatyka","course-level":"level1","course-type":"stacjonarne"}
    - form_get_field_of_study_limits
    - form{"name":"form_get_field_of_study_limits"}
    - form{"name":null}

## base + field_of_study 2
* greet
  - utter_greet
  - action_general_options
* field_of_study_limits{"field-of-study":"fizyka","course-level":"level2","course-type":"niestacjonarne"}
    - form_get_field_of_study_limits
    - form{"name":"form_get_field_of_study_limits"}
    - form{"name":null}

## about_limits multiple requests
* greet
    - utter_greet
    - action_general_options
* field_of_study_limits{"field-of-study":"informatyka","course-level":"level1","course-type":"stacjonarne"}
    - form_get_field_of_study_limits
    - form{"name":"form_get_field_of_study_limits"}
    - form{"name":null}
* field_of_study_limits{"field-of-study":"matematyka","course-level":"level2","course-type":"niestacjonarne"}
    - form_get_field_of_study_limits
    - form{"name":"form_get_field_of_study_limits"}
    - form{"name":null}
* field_of_study_limits{"field-of-study":"fizyka","course-level":"level1","course-type":"niestacjonarne"}
    - form_get_field_of_study_limits
    - form{"name":"form_get_field_of_study_limits"}
    - form{"name":null}
*  goodbye
    - utter_goodbye