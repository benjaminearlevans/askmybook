import requests

from resemble.stream_decoder import StreamDecoder

V2_STREAMING_BUFFER_SIZE = 4 * 1024
V2_STREAMING_CHUNK_SIZE = 2

class Resemble:
	_token = None
	_base_url = 'https://app.resemble.ai/api/'
	_headers = { 'Content-Type': 'application/json', 'Authorization': f"Token token={_token}" }

	_syn_server_url = None
	_syn_server_headers = { 'Content-Type': 'application/json', 'x-access-token': f"{_token}" }

	@staticmethod
	def api_key(api_key):
		Resemble._token = api_key
		Resemble._headers['Authorization'] = f"Token token={Resemble._token}"
		Resemble._syn_server_headers['x-access-token'] = f"{Resemble._token}"

	@staticmethod
	def base_url(url):
		Resemble._base_url = url
	
	@staticmethod
	def endpoint(version, endpoint):
		api_endpoint = endpoint if endpoint.startswith('/') else f"/{endpoint}"
		return f"{Resemble._base_url}{version}{api_endpoint}"

	@staticmethod
	def syn_server_url(url):
		url = url if url.endswith('/') else f"{url}/"
		Resemble._syn_server_url = url

	@staticmethod
	def syn_server_endpoint(endpoint):
		if Resemble._syn_server_url is None:
			raise ValueError("Please initialize the synthesis server url by calling Resemble.syn_server_url before "
							 "using the streaming API. If you're not sure what your streaming URL is, "
							 "please contact team@resemble.ai. The Streaming API is currently in beta and is not "
							 "available to all users. Please reach out to team@resemble.ai to inquire more.")
		api_endpoint = endpoint[:-1] if endpoint.startswith('/') else endpoint
		return f"{Resemble._syn_server_url}{api_endpoint}"

	class _V2:
		class _ProjectsV2:
			def all(self, page: int, page_size: int = None):
				query = { 'page': page }
				if page_size:
					query['page_size'] = page_size
				r = requests.get(Resemble.endpoint('v2', 'projects'), headers=Resemble._headers, params=query)
				return r.json()

			def create(self, name: str, description: str, is_public: bool = False, is_collaborative: bool = False, is_archived: bool = False):
				r = requests.post(Resemble.endpoint('v2', 'projects'), headers=Resemble._headers, json={
					'name': name,
					'description': description,
					'is_public': is_public,
					'is_collaborative': is_collaborative,
					'is_archived': is_archived
				})
				return r.json()

			def update(self, uuid: str, name: str, description: str, is_public: bool = False, is_collaborative: bool = False, is_archived: bool = False):
				r = requests.put(Resemble.endpoint('v2', f"projects/{uuid}"), headers=Resemble._headers, json={
					'name': name,
					'description': description,
					'is_public': is_public,
					'is_collaborative': is_collaborative,
					'is_archived': is_archived
				})
				return r.json()

			def get(self, uuid: str):
				r = requests.get(Resemble.endpoint('v2', f"projects/{uuid}"), headers=Resemble._headers)
				return r.json()

			def delete(self, uuid: str):
				r = requests.delete(Resemble.endpoint('v2', f"projects/{uuid}"), headers=Resemble._headers)
				return r.json()

		class _VoicesV2:
			def all(self, page: int, page_size: int = None):
				query = { 'page': page }
				if page_size:
					query['page_size'] = page_size
				r = requests.get(Resemble.endpoint('v2', 'voices'), headers=Resemble._headers, params=query)
				return r.json()

			def create(self, name: str, dataset_url: str = None, callback_uri: str = None):
				json = {
					'name': name
				}
				if dataset_url:
					json['dataset_url'] = dataset_url
				if callback_uri:
					json['callback_uri'] = callback_uri
				r = requests.post(Resemble.endpoint('v2', 'voices'), headers=Resemble._headers, json=json)
				return r.json()

			def update(self, uuid: str, name: str, dataset_url: str = None):
				json = {
					'name': name
				}
				if dataset_url:
					json['dataset_url'] = dataset_url
				r = requests.put(Resemble.endpoint('v2', f"voices/{uuid}"), headers=Resemble._headers, json=json)
				return r.json()
				
			def build(self, uuid: str):
				r = requests.post(Resemble.endpoint('v2', f"voices/{uuid}/build", headers=Resemble._headers))
				return r.json()

			def get(self, uuid: str):
				r = requests.get(Resemble.endpoint('v2', f"voices/{uuid}"), headers=Resemble._headers)
				return r.json()

			def delete(self, uuid: str):
				r = requests.delete(Resemble.endpoint('v2', f"voices/{uuid}"), headers=Resemble._headers)
				return r.json()

		class _ClipsV2:
			def all(self, project_uuid: str, page: int, page_size: int = None):
				query = { 'page': page }
				if page_size:
					query['page_size'] = page_size
				r = requests.get(Resemble.endpoint('v2', f"projects/{project_uuid}/clips"), headers=Resemble._headers, params=query)
				return r.json()

			def create_sync(self, project_uuid: str, voice_uuid: str, body: str, title: str = None, sample_rate: int = None, output_format: str = None, precision: str = None, include_timestamps: bool = None, is_public: bool = None, is_archived: bool = None, raw: bool = None):
				options = {k: v for k, v in ({
					'voice_uuid': voice_uuid,
					'body': body,
					'title': title,
					'sample_rate': sample_rate,
					'output_format': output_format,
					'precision': precision,
					'include_timestamps': include_timestamps,
					'is_public': is_public,
					'is_archived': is_archived,
					'raw': raw
				}).items() if v is not None}

				r = requests.post(Resemble.endpoint('v2', f"projects/{project_uuid}/clips"), headers=Resemble._headers, json=options)
				return r.json()

			def create_async(self, project_uuid: str, voice_uuid: str, callback_uri: str, body: str, title: str = None, sample_rate: int = None, output_format: str = None, precision: str = None, include_timestamps: bool = None, is_public: bool = None, is_archived: bool = None):
				options = {k: v for k, v in ({
					'voice_uuid': voice_uuid,
					'body': body,
					'title': title,
					'sample_rate': sample_rate,
					'output_format': output_format,
					'precision': precision,
					'include_timestamps': include_timestamps,
					'is_public': is_public,
					'is_archived': is_archived,
					'callback_uri': callback_uri
				}).items() if v is not None}

				r = requests.post(Resemble.endpoint('v2', f"projects/{project_uuid}/clips"), headers=Resemble._headers, json=options)
				return r.json()

			def update_async(self, project_uuid: str, clip_uuid: str, voice_uuid: str, callback_uri: str, body: str, title: str = None, sample_rate: int = None, output_format: str = None, precision: str = None, include_timestamps: bool = None, is_public: bool = None, is_archived: bool = None):
				options = {k: v for k, v in ({
					'voice_uuid': voice_uuid,
					'body': body,
					'title': title,
					'sample_rate': sample_rate,
					'output_format': output_format,
					'precision': precision,
					'include_timestamps': include_timestamps,
					'is_public': is_public,
					'is_archived': is_archived,
					'callback_uri': callback_uri
				}).items() if v is not None}
				
				r = requests.put(Resemble.endpoint('v2', f"projects/{project_uuid}/clips/{clip_uuid}"), headers=Resemble._headers, json=options)
				return r.json()

			def stream(self, project_uuid: str, voice_uuid: str, body: str, buffer_size: int = V2_STREAMING_BUFFER_SIZE, ignore_wav_header=True):
				options = {
					"project_uuid": project_uuid,
					"voice_uuid": voice_uuid,
					"data": body
				}
				r = requests.post(Resemble.syn_server_endpoint('stream'), headers=Resemble._syn_server_headers, json=options, stream=True)
				r.raise_for_status()
				stream_decoder = StreamDecoder(buffer_size, ignore_wav_header)
				# Iterate over the stream and start decoding, and returning data
				for chunk in r.iter_content(chunk_size=V2_STREAMING_CHUNK_SIZE):
					if chunk:
						stream_decoder.decode_chunk(chunk)
						buffer = stream_decoder.flush_buffer()
						if buffer:
							yield buffer

				# Keep draining the buffer until the len(buffer) < buffer_size or len(buffer) == 0
				buffer = stream_decoder.flush_buffer()
				while buffer is not None:
					buff_to_return = buffer
					buffer = stream_decoder.flush_buffer()
					yield buff_to_return

				# Drain any leftover content in the buffer, len(buffer) will always be less than buffer_size here
				buffer = stream_decoder.flush_buffer(force=True)
				if buffer:
					yield buffer

			def get(self, project_uuid: str, clip_uuid: str):
				r = requests.get(Resemble.endpoint('v2', f"projects/{project_uuid}/clips/{clip_uuid}"), headers=Resemble._headers)
				return r.json()

			def delete(self, project_uuid: str, clip_uuid: str):
				r = requests.delete(Resemble.endpoint('v2', f"projects/{project_uuid}/clips/{clip_uuid}"), headers=Resemble._headers)
				return r.json()

		class _RecordingsV2:
			def all(self, voice_uuid: str, page: int, page_size: int = None):
				query = { 'page': page }
				if page_size:
					query['page_size'] = page_size
				r = requests.get(Resemble.endpoint('v2', f"voices/{voice_uuid}/recordings"), headers=Resemble._headers, params=query)
				return r.json()

			def create(self, voice_uuid: str, file, name: str, text: str, is_active: bool, emotion: str):
				r = requests.post(Resemble.endpoint('v2', f"voices/{voice_uuid}/recordings"), headers={'Authorization': Resemble._headers['Authorization']}, files={
					'file': file,
				}, json={
					'name': name,
					'text': text,
					'is_active': is_active,
					'emotion': emotion
				})
				return r.json()

			def update(self, voice_uuid: str, recording_uuid: str, name: str, text: str, is_active: bool, emotion: str):
				r = requests.put(Resemble.endpoint('v2', f"voices/{voice_uuid}/recordings/{recording_uuid}"), headers=Resemble._headers, json={
					'name': name,
					'text': text,
					'is_active': is_active,
					'emotion': emotion
				})
				return r.json()

			def get(self, voice_uuid: str, recording_uuid: str):
				r = requests.get(Resemble.endpoint('v2', f"voices/{voice_uuid}/recordings/{recording_uuid}"), headers=Resemble._headers)
				return r.json()

			def delete(self, voice_uuid: str, recording_uuid: str):
				r = requests.delete(Resemble.endpoint('v2', f"voices/{voice_uuid}/recordings/{recording_uuid}"), headers=Resemble._headers)
				return r.json()

		projects = _ProjectsV2()
		clips = _ClipsV2()
		voices = _VoicesV2()
		recordings = _RecordingsV2()
	
	v2 = _V2()

