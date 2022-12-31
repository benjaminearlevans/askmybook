STREAMING_WAV_HEADER_BUFFER_LEN = 44


class StreamDecoder():
    def __init__(self, buffer_size, ignore_wav_header):
        if buffer_size < 2:
            raise ValueError("Buffer size cannot be less than 2")

        if buffer_size % 2 != 0:
            raise ValueError("Buffer size must be evenly divisible by 2.")

        self.buffer_size = buffer_size
        self.ignore_wav_header = ignore_wav_header
        self.header_buffer = bytearray()
        self.buffer = bytearray()

    def decode_chunk(self, chunk):
        if len(self.header_buffer) < STREAMING_WAV_HEADER_BUFFER_LEN and self.ignore_wav_header:
            self.header_buffer.extend(chunk)
            if len(self.header_buffer) >= STREAMING_WAV_HEADER_BUFFER_LEN:
                self.buffer = self.header_buffer[STREAMING_WAV_HEADER_BUFFER_LEN:]
                self.header_buffer = self.header_buffer[0:STREAMING_WAV_HEADER_BUFFER_LEN]
        else:
            self.buffer.extend(chunk)

    def flush_buffer(self, force=False):
        if force:
            return_buffer = self.buffer[0:]
            self.buffer = []
            return return_buffer
        if len(self.buffer) >= self.buffer_size:
            # only get the request buffer size from the stored buffer
            return_buffer = self.buffer[0:self.buffer_size]
            # This removes the current buffer being returned from the stored buffer
            self.buffer = self.buffer[self.buffer_size:]
            return return_buffer
        return None

    @staticmethod
    def __byte_to_int(bytes):
        return int.from_bytes(bytes, byteorder='little')
