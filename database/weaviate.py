import weaviate

vdb_client = weaviate.connect_to_local()
print("Connected to Weviate: ", vdb_client.is_ready())
