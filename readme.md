# Spring Entity Generator

Makes creating Spring Entity, Controller and Repositories simple.


## Running the script:

### Default, will generate controller, will not generate audit model
`spring_entity_gen.py "Book Author" com.pak.age`

### Will generate controller, and audit model
`spring_entity_gen.py "Book Author" com.pak.age audit_model`

### Without Controller
`spring_entity_gen.py "Book Author" com.pak.age skp_cnt`

### With AuditModel 
`spring_entity_gen.py "Book Author" com.pak.age skp_cnt audit_model`
