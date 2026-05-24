# GatewaySentry Bypass . Dev > L.A.T <
import requests
import json
import base64
import zlib
import struct
import random
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Hash import SHA1
from Crypto.Random import get_random_bytes

# GatewaySentry RSA Public Key
PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyZCQRWc6hi6OMJ6Hy8Cu
McZ2kdJYkcG2qaY+dqyhkqpEpGa0Fn+ZZSqgUAQwSMi18DFShTIJ+WRq8XUGoQhX
IbeZeWJKeyQu8+syKnYFDDdn3BZDuBUQel+Ny3A+73T7qhmKbLMrALCzqB2DCtzu
PNXc8woics42eNUTWYPwAqcKkIOlhQFRKwj6mTlmrpwLycWJr/L7Fhkk5GlKdzSS
D3uBicBZL0XJlEUBvwnF4Azdggvj1u/qUM5FVh3971MiGePXlYn9pGO9v5tCxvN0
HhSwO7/iLYtcF22s4EsjN4UlKv4dJCnSXLhZksGAvdaoxNm2YXLfjuAp2iGtGeTg
rwIDAQAB
-----END PUBLIC KEY-----"""

DEVICE_FINGERPRINT = "23f4693f"

class SimplePNGParser:
    def __init__(self, base64_data):
        if ',' in base64_data:
            base64_data = base64_data.split(',')[1]
        self.data = base64.b64decode(base64_data)
        self.pos = 0

    def read(self, n):
        chunk = self.data[self.pos:self.pos + n]
        self.pos += n
        return chunk

    def parse(self):
        self.pos = 0
        if self.read(8) != b'\x89PNG\r\n\x1a\n':
            return 0

        idat_data = b''
        width = 0
        height = 0
        color_type = 0

        while self.pos < len(self.data):
            try:
                length = struct.unpack('>I', self.read(4))[0]
                chunk_type = self.read(4)
                chunk_data = self.read(length)
                self.read(4)

                if chunk_type == b'IHDR':
                    width, height, _, color_type, _, _, _ = struct.unpack('>IIBBBBB', chunk_data)
                elif chunk_type == b'IDAT':
                    idat_data += chunk_data
                elif chunk_type == b'IEND':
                    break
            except:
                break

        if not idat_data:
            return 0
        try:
            decompressed = zlib.decompress(idat_data)
        except:
            return 0

        bpp = 4 if color_type == 6 else 3
        scanline_len = 1 + width * bpp
        mass = 0

        try:
            for y in range(height):
                idx = y * scanline_len + 1
                row = decompressed[idx: idx + width * bpp]
                for i in range(0, len(row), bpp):
                    if row[i] < 250 or (bpp > 1 and row[i + 1] < 250):
                        mass += 1
        except:
            pass
        return mass

def generate_telemetry():
    now_ms = int(time.time() * 1000)
    dwell = random.randint(2500, 8500)

    moves_count = random.randint(30, 100)
    moves = []
    start_x = random.randint(100, 500)
    start_y = random.randint(100, 500)

    for i in range(moves_count):
        start_x += random.randint(-5, 5)
        start_y += random.randint(-5, 5)
        time_offset = int((i / moves_count) * dwell)
        moves.append([start_x, start_y, time_offset])

    speed_samples = [random.randint(100, 2000) for _ in range(moves_count)]

    telemetry = {
        "dwellMs": dwell,
        "moves": moves,
        "velocityVar": round(random.uniform(100, 500), 6),
        "velocityMedian": round(random.uniform(50, 150), 6),
        "velocityAvg": round(random.uniform(100, 300), 6),
        "velocityMin": round(random.uniform(0.1, 5), 6),
        "velocityMax": round(random.uniform(800, 1500), 6),
        "velocityP25": round(random.uniform(20, 60), 6),
        "velocityP75": round(random.uniform(200, 400), 6),
        "directionChanges": random.randint(5, 15),
        "keypresses": [],
        "speedSamples": speed_samples,
        "moveDensity": round(random.uniform(10, 30), 6)
    }

    path = {
        "moves": moves,
        "totalDist": random.randint(500, 2000),
        "durationMs": dwell / 1000.0,
        "avgSpeed": random.uniform(100, 500),
        "clickTimestamp": now_ms,
        "timeToFirstClick": random.randint(500, 2000)
    }
    return telemetry, path

def encrypt_payload(public_key, data):
    json_str = json.dumps(data, separators=(',', ':'))
    data_bytes = json_str.encode('utf-8')
    
    session_key = get_random_bytes(32)
    iv = get_random_bytes(12)
    
    cipher_aes = AES.new(session_key, AES.MODE_GCM, nonce=iv)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data_bytes)
    
    rsa_key = RSA.importKey(public_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_key, hashAlgo=SHA1)
    encrypted_session_key = cipher_rsa.encrypt(session_key)
    
    final_blob = encrypted_session_key + iv + ciphertext + tag
    return base64.b64encode(final_blob).decode('utf-8')

def solve_captcha():
    GatewaySentry_URL = "https://sentry.platorelay.com"

    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "text/plain;charset=UTF-8",
        "origin": "https://sentry.platorelay.com",
        "referer": "https://sentry.platorelay.com/a?d=NIGGA-GatewaySentry",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    session = requests.Session()

    print("1. Requesting Puzzle...")

    tele_req, _ = generate_telemetry()

    req_payload = {
        "telemetry": tele_req,
        "deviceFingerprint": DEVICE_FINGERPRINT,
        "forcePuzzle": True
    }

    encrypted_body = encrypt_payload(PUBLIC_KEY, req_payload)
    print(f"Payload Length: {len(encrypted_body)}")

    try:
        resp = session.post(
            f"{GatewaySentry_URL}/.gs/pow/captcha/request",
            headers=headers,
            data=encrypted_body,
            timeout=10
        )

        if resp.status_code != 200:
            print(f"Status: {resp.status_code}")
            print(f"Response: {resp.text}")
            return

        data = resp.json()

    except Exception as e:
        print(f"Request Error: {e}")
        return

    puzzle_id = data.get('data', {}).get('id') or data.get('id')
    puzzle = data.get('data', {}).get('puzzle', {}) or data.get('puzzle', {})
    instruction = puzzle.get('instruction', '')
    shapes = puzzle.get('shapes', [])

    if not puzzle_id:
        print("No puzzle returned (maybe passed directly?)")
        print(data)
        return

    print(f"ID: {puzzle_id}")
    print(f"Task: {instruction}")

    analyzed = []
    for i, shape_obj in enumerate(shapes):
        img_data = shape_obj.get('img') or shape_obj.get('image', '')
        if not img_data:
            continue

        parser = SimplePNGParser(img_data)
        mass = parser.parse()
        analyzed.append({'index': i, 'mass': mass})
        print(f"Shape {i}: mass={mass}")

    if not analyzed:
        print("Error analyzing shapes")
        return

    if "smallest" in instruction.lower():
        winner = min(analyzed, key=lambda x: x['mass'])
    else:
        winner = max(analyzed, key=lambda x: x['mass'])

    target_index = winner['index']
    print(f"Answer: {target_index}")

    print("\n2. Verifying...")
    tele_verify, path_verify = generate_telemetry()

    verify_payload = {
        "id": puzzle_id,
        "answers": [str(target_index)],
        "path": path_verify,
        "telemetry": tele_verify,
        "deviceFingerprint": DEVICE_FINGERPRINT
    }

    encrypted_verify = encrypt_payload(PUBLIC_KEY, verify_payload)

    try:
        v_resp = session.post(
            f"{GatewaySentry_URL}/.gs/pow/captcha/verify",
            headers=headers,
            data=encrypted_verify,
            timeout=10
        )
        print(f"Verify Status: {v_resp.status_code}")
        print(f"Verify Result: {v_resp.text}")
    except Exception as e:
        print(f"Verify Error: {e}")

if __name__ == '__main__':
    solve_captcha()