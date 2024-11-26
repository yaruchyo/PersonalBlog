from flaskblog.service_layer.storage_repository.filebase_service import FileBaseStorage


file_storage= FileBaseStorage()

def test_retrieve_all_names():
	response = file_storage.list_all_files()
	return response
def test_delete_all_files():
	names = test_retrieve_all_names()
	for name in names:
		file_storage.delete(name['Key'])

