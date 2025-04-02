# Assignment notes

## Solution

The files for a solution are held in the `solution` folder.



## Environment

`$ pyenv install 3.11.11`

`$ pyenv local 3.11.11`

`$ python -m venv .venv`

`$ source .venv\bin\activate`

## Diagram
Using: https://mermaid.js.org/

Relationships are in: References.SemanticModel/definition/relationships.tmdl

```mermaid
    erDiagram
    ref_references }|--|{ ref_job_positions : job_position_id
    ref_user_tags }|--|{ ref_job_positions : job_position_id
    ref_assigned_to }|--|{ ref_job_positions : job_position_id
    ref_references }|--|{ Dates : Date
    
    Dates {
        string Date
        string Year
        string Month_Year
        string MonthYearId
        string FirstDayofMonth 
        }
    
    ref_assigned_to {
        int64 job_position_id
        string assigned_to 
        }
    
    ref_job_positions {
        int64 job_position_id
        string role
        string job_position_status
        bool signed_off
        int64 organisation_id 
        }
    
    ref_references {
        int64 completed_to_reviewed_days
        string completed_to_reviewed_time
        string cr_created_at
        int64 job_position_id
        string marked_compliant_at
        string ref_approval_status
        string ref_approved_at
        string ref_approved_date
        string ref_completed_at
        string ref_completed_date
        string ref_requested_at
        string ref_requested_date
        string ref_status
        int64 requested_to_completed_days
        string requested_to_completed_time
        int64 requested_to_compliant_days
        string requested_to_compliant_time
        string requested_to_reviewed_days
        string requested_to_reviewed_time
        bool is_mandatory 
        }
    
    ref_user_tags {
        int64 job_position_id
        string tag 
        }
```


