"""Anthropic adapter (contracts section 1.4).

Generator: Claude. Embedding/reranking: Anthropic has no first-party embedding
model, so the embedding/reranker selection resolves to the configured fallback
(default local), recorded as embedding.resolved_from in the manifest. That
resolution happens in the factory; this module provides only the Claude
generator. The key is sourced via resolve_secret and a missing key raises
MissingSecretError at construction.
"""

from __future__ import annotations

from providers.base import GenerationResult, MissingSecretError
from providers.secrets import resolve_secret

# Indicative public per-token pricing (USD) for cost accounting. Pinned here so
# cost_usd is reproducible; update alongside the model id. Opus 4.8: $5/$25 per MTok.
_INPUT_USD_PER_TOKEN = 5.0 / 1_000_000
_OUTPUT_USD_PER_TOKEN = 25.0 / 1_000_000

# Model families that reject sampling parameters (temperature/top_p/top_k) and
# the legacy thinking budget. The contract Generator signature still accepts
# temperature, but for these models it is not forwarded to the API (a 400).
_NO_SAMPLING_PREFIXES = ("claude-opus-4-8", "claude-opus-4-7", "claude-fable-5")


class AnthropicGenerator:
    name = "anthropic"

    def __init__(self, model: str = "claude-opus-4-8") -> None:
        api_key = resolve_secret("ANTHROPIC_API_KEY")
        if not api_key:
            raise MissingSecretError(
                "ANTHROPIC_API_KEY is required for the anthropic generator adapter."
            )
        self._model = model
        try:
            import anthropic  # type: ignore
        except Exception as exc:  # noqa: BLE001
            raise MissingSecretError(
                "The 'anthropic' SDK is not installed; install the 'cloud' extra."
            ) from exc
        self._client = anthropic.Anthropic(api_key=api_key)

    @staticmethod
    def _cost(prompt_tokens: int, completion_tokens: int) -> float:
        cost = prompt_tokens * _INPUT_USD_PER_TOKEN + completion_tokens * _OUTPUT_USD_PER_TOKEN
        return round(cost, 6)

    def generate(
        self,
        *,
        system: str,
        messages: list[dict],
        temperature: float = 0.0,
        max_tokens: int = 1024,
        stop: list[str] | None = None,
    ) -> GenerationResult:
        kwargs: dict = {
            "model": self._model,
            "system": system,
            "messages": messages,
            "max_tokens": max_tokens,
            "stop_sequences": stop or [],
        }
        # Sampling params are rejected (400) on the Opus 4.7+/Fable families.
        if not self._model.startswith(_NO_SAMPLING_PREFIXES):
            kwargs["temperature"] = temperature
        response = self._client.messages.create(**kwargs)
        text = "".join(
            block.text for block in response.content if getattr(block, "type", "") == "text"
        )
        prompt_tokens = int(response.usage.input_tokens)
        completion_tokens = int(response.usage.output_tokens)
        finish = response.stop_reason or "stop"
        finish_reason = {"end_turn": "stop", "max_tokens": "length"}.get(finish, finish)
        return GenerationResult(
            text=text,
            model=self._model,
            model_version=self._model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost_usd=self._cost(prompt_tokens, completion_tokens),
            finish_reason=finish_reason,
            raw_meta={"adapter": "anthropic", "stop_reason": finish},
        )

    def health(self) -> dict:
        return {"ok": True, "model": self._model, "detail": "anthropic"}
