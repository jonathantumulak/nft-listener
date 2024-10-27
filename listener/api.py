from typing import Type

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from web3 import Web3
from web3.contract import Contract


ABI = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "from", "type": "address"},
            {"indexed": True, "name": "to", "type": "address"},
            {"indexed": True, "name": "tokenId", "type": "uint256"},
        ],
        "name": "Transfer",
        "type": "event",
    }
]


class InfuraAPI:
    def __init__(self):
        self._check_settings("INFURA_URL")
        self._check_settings("INFURA_API_KEY")
        self._check_settings("INFURA_API_KEY")

        infura_url = f"{settings.INFURA_URL}{settings.INFURA_API_KEY}"
        self.w3 = Web3(Web3.HTTPProvider(infura_url))

    @staticmethod
    def _check_settings(key: str) -> None:
        """Check settings key if configured correctly"""
        value = getattr(settings, key, None)
        if value is None:
            raise ImproperlyConfigured(f"Missing {key}")
        elif value == "":
            raise ImproperlyConfigured(f"{key} cannot be empty.")

    def _get_contract(
        self,
        contract_address: str = None,
        abi: list[dict] = None,
    ) -> Type[Contract]:
        if not contract_address:
            contract_address = settings.CONTRACT_ADDRESS

        if not abi:
            abi = ABI
        return self.w3.eth.contract(address=contract_address, abi=abi)

    def get_contract_events(
        self,
        start_block: int,
        end_block: int,
        contract_address: str = None,
        abi: list[dict] = None,
    ) -> list[dict]:
        """Function to get contract transfer events"""
        contract = self._get_contract(contract_address, abi)
        events = contract.events.Transfer.create_filter(
            from_block=start_block, to_block=end_block
        ).get_all_entries()

        return events
