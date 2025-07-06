from dunetuf.job.job_history.job_history import JobHistory
from dunetuf.job.job_queue.job_queue import JobQueue
from dunetuf.print.print_new import Print
import logging
def clear_and_verify_event_cleared(udw,expected_events):
    eng = engine.Enginelib(self.udw)
    assert expected_events == eng.getNewEventsLogged(cleared_event_log), "Event is not cleared successfully"

class TestWhenPrintingJPEGFile():
    @classmethod
    def setup_class(cls):
        cls.job_queue = JobQueue()
        cls.job_history = JobHistory()
        cls.print = Print()

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self):
        self.job_queue.cancel_all_jobs()
        self.job_queue.wait_for_queue_empty()

        # Clear job history
        #TODO: Create job_history methods in Ares
        #self.job_history.clear()
        #self.job_history.wait_for_history_empty()

    def teardown_method(self):
        self.job_queue.cancel_all_jobs()
        self.job_queue.wait_for_queue_empty()

        # Clear job history
        #TODO: Create job_history methods in Ares
        #self.job_history.clear()
        #self.job_history.wait_for_history_empty()

    """

    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Event code via JPEG verysmall.jpg file
        +test_tier: 1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-24060
        +timeout:360
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:verysmall.jpg=fc878bdbba4f8f6d58eaa76d28459fbbe4ef400a43eb85f43933245c3271a163
        +name:TestWhenPrintingJPEGFile::test_when_using_pdlmh_printablewidth_zero_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_pdlmh_printablewidth_zero
            +guid:4d21efa6-1e37-41a5-aedd-4f382a164cc2
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=JPEG & EngineFirmwareFamily=Canon
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$

    """
    def test_when_using_pdlmh_printablewidth_zero_then_succeeds(self):
            job_id = self.print.raw.start('fc878bdbba4f8f6d58eaa76d28459fbbe4ef400a43eb85f43933245c3271a163')
            # Wait for copy job to complete
            self.print.wait_for_state(job_id, ["completed"])
            event_code = "F0.01.08.1C"
            response = self.cdm.get_raw(self.cdm.WARNING_EVENT_LOG_ENDPOINT)
            warning_events = response.json().get("events", [])

            event_found = False

            if warning_events is None:
                print("Test Failed: Event code not found.")

            for event in warning_events:
                if event.get("eventCode") == event_code:
                    event_found = True
                    break 

            assert event_found, f"Test Failed: Event code {event_code} not found."
            print("Test Passed: Event code found.")
