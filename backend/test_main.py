import unittest
from unittest.mock import patch

import httpx
from fastapi.testclient import TestClient

import main


class AskTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(main.app)
        self.async_client = httpx.AsyncClient

    def transport(self, handler):
        return patch("main.httpx.AsyncClient", side_effect=lambda **kwargs: self.async_client(
            transport=httpx.MockTransport(handler), **kwargs
        ))

    def test_modes_send_correct_instruction_and_trim_question(self):
        import json
        for mode in main.PROMPTS:
            with self.subTest(mode=mode):
                def handler(request):
                    body = json.loads(request.content)
                    self.assertIn(main.PROMPTS[mode], body["messages"][0]["content"])
                    self.assertEqual(body["messages"][1]["content"], "What is an index?\n/no_think")
                    self.assertFalse(body["think"])
                    return httpx.Response(200, json={"message": {"content": " An index speeds up reads. "}})
                with self.transport(handler):
                    response = self.client.post("/ask", json={"question": " What is an index? ", "mode": mode})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json()["answer"], "An index speeds up reads.")

    def test_invalid_inputs_do_not_call_ollama(self):
        with patch("main.httpx.AsyncClient") as client:
            for body in [{"question": " "}, {"question": "x" * 4001},
                         {"question": "index", "mode": "unknown"}, {}]:
                self.assertEqual(self.client.post("/ask", json=body).status_code, 422)
            client.assert_not_called()

    def test_qwen_reasoning_prefix_is_not_returned(self):
        for text in ["<think>private reasoning</think>Final answer", "reasoning</think>Final answer"]:
            with self.transport(lambda request: httpx.Response(200, json={"message": {"content": text}})):
                self.assertEqual(self.client.post("/ask", json={"question": "index"}).json()["answer"], "Final answer")

    def test_unreachable_model(self):
        def handler(request):
            raise httpx.ConnectError("offline", request=request)
        with self.transport(handler):
            self.assertEqual(self.client.post("/ask", json={"question": "index"}).status_code, 503)

    def test_timeout(self):
        def handler(request):
            raise httpx.ReadTimeout("slow", request=request)
        with self.transport(handler):
            self.assertEqual(self.client.post("/ask", json={"question": "index"}).status_code, 504)

    def test_empty_or_truncated_answer(self):
        for result in [{"message": {"content": " "}},
                       {"message": {"content": "partial"}, "done_reason": "length"}]:
            with self.transport(lambda request: httpx.Response(200, json=result)):
                self.assertEqual(self.client.post("/ask", json={"question": "index"}).status_code, 502)

    def test_health_checks_model_availability(self):
        for models, status in [([], 503), ([{"name": main.MODEL}], 200)]:
            with self.transport(lambda request: httpx.Response(200, json={"models": models})):
                self.assertEqual(self.client.get("/health").status_code, status)


if __name__ == "__main__":
    unittest.main()
