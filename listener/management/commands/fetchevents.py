from django.core.management.base import (
    BaseCommand,
    CommandError,
    CommandParser,
)
from listener.api import InfuraAPI
from listener.models import TransferEvent
from web3.exceptions import Web3Exception


class Command(BaseCommand):
    help = "Fetches Transfer contract events and save the to database"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--start_block", type=int, default=None)
        parser.add_argument("--end_block", type=int, default=None)

    def handle(self, *args, **options) -> None:
        start_block = options["start_block"]
        if start_block is None:
            raise CommandError("start_block is required")

        end_block = options["end_block"]
        if end_block is None:
            raise CommandError("end_block is required")

        api = InfuraAPI()

        try:
            events = api.get_contract_events(start_block, end_block)
        except Web3Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Fetch events encountered an error: {str(e)}")
            )
            return

        self.stdout.write(
            self.style.SUCCESS(f"Found {len(events)} transfer events.")
        )

        if len(events) > 0:
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
