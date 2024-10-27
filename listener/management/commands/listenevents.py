import asyncio

from django.core.management.base import BaseCommand
from listener.api import InfuraAPI
from listener.models import TransferEvent
from web3.exceptions import Web3Exception


class Command(BaseCommand):
    help = "Listens for new Transfer contract events and save them to database"

    async def fetch_loop(self, api: InfuraAPI, poll_interval: int) -> None:
        """Fetch new contract events and save them to database"""
        while True:
            try:
                events = api.get_new_contract_events()
            except Web3Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Fetch events encountered an error: {str(e)}"
                    )
                )
                return
            if len(events) > 0:
                self.stdout.write(
                    self.style.SUCCESS(f"Found {len(events)} transfer events.")
                )
                self.stdout.write(self.style.NOTICE("Saving to db.."))
                transfer_events = []
                for event in events:
                    event_args = event["args"]
                    transfer_events.append(
                        TransferEvent(
                            token_id=event_args["tokenId"],
                            from_address=event_args["from"],
                            to_address=event_args["to"],
                            tx_hash=event["transactionHash"].to_0x_hex(),
                            block_number=event["blockNumber"],
                        )
                    )
                TransferEvent.objects.bulk_create(transfer_events)
                self.stdout.write(self.style.SUCCESS("Done!"))
            else:
                self.stdout.write("No transfer events found.")
            await asyncio.sleep(poll_interval)

    def handle(self, *args, **options) -> None:
        """Start event loop"""
        api = InfuraAPI()

        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(asyncio.gather(self.fetch_loop(api, 2)))
        finally:
            loop.close()
