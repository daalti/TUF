from dunetuf.job.job_history.job_history import JobHistory
from dunetuf.job.job_queue.job_queue import JobQueue
from dunetuf.print.print_new import Print
import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType, MediaOrientation

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
        +purpose:Simple print job of Jpeg TestSuite faces small Page from *faces_small.jpg file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:faces_small.jpg=19d6b2e4af3faca6ef1c95c5750a3c8dea079b14a04a061cf4d2acdfaf2cb9fc
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_testsuite_faces_small_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_testsuite_faces_small
            +guid:48fd8a11-adc9-41bc-a33e-12b4f326d772
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG
    

        +overrides:
            +Enterprise:
                +is_manual:False
                +timeout:600
                +test:
                    +dut:
                        +type:Emulator
    

    

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$

    """
    def test_when_using_testsuite_faces_small_then_succeeds(self):
            default = self.tray.get_default_source()
            if self.print_emulation.print_engine_platform == 'emulator' and self.configuration.familyname == 'enterprise':
                tray1 = MediaInputIds.Tray1.name
                if self.tray.is_size_supported('anycustom', 'tray-1'):
                    self.print_emulation.tray.open(tray1)
                    self.print_emulation.tray.load(tray1, MediaSize.Custom.name, MediaType.Plain.name)
                    self.print_emulation.tray.close(tray1)
            else:
                if self.tray.is_size_supported('anycustom', default):
                    self.tray.configure_tray(default, 'anycustom', 'stationery')
                else:
                    self.tray.configure_tray(default, 'custom', 'stationery')

            job_id = self.print.raw.start('19d6b2e4af3faca6ef1c95c5750a3c8dea079b14a04a061cf4d2acdfaf2cb9fc')
            # Wait for copy job to complete
            self.print.wait_for_state(job_id, ["completed"])
            self.outputsaver.save_output()
            self.tray.reset_trays()

            logging.info("JPEG TestSuite faces small Page - Print job completed successfully")
