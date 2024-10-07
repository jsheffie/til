```python
import uuid

# Generate a UUIDv4
unique_id = uuid.uuid4()

# Print the UUID
print(unique_id)

25bfd7f3-9683-4346-a224-ae6e62ac805c
```


Some fun code

```python
import uuid

for i in range(1, 10000):
    random_uuid = f"{uuid.uuid4()}-{uuid.uuid4()}"
    parts = str(random_uuid).split('-')
    var = "-".join(sorted(parts))
    print(f"{var[:55]}")
```