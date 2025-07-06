from dunetuf.job.job_history.job_history import JobHistory
from dunetuf.job.job_queue.job_queue import JobQueue
from dunetuf.print.print_new import Print
import logging
from dunetuf.print.print_common_types import MediaType, MediaOrientation

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
        +purpose: Simple Print job of Jpeg file of 1MB from **
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:file_example_JPG_1MB.jpg=683a8528125ca09d8314435c051331de2b4c981c756721a2d12c103e8603a1d2
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_file_example_JPG_1MB_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_file_example_JPG_1MB
            +guid:53177689-80cf-4d01-af66-5985b006b309
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
    def test_when_using_file_example_JPG_1MB_then_succeeds(self):
            if self.print_emulation.print_engine_platform == 'emulator' and self.configuration.familyname == 'enterprise':
                installed_trays = self.print_emulation.tray.get_installed_trays()
                selected_tray = None

                # Check each tray for supported sizes
                for tray_id in installed_trays:
                    system_tray_id = tray_id.lower().replace('tray', 'tray-')
                    if self.tray.is_size_supported('anycustom', system_tray_id):
                        selected_tray = tray_id
                        self.print_emulation.tray.open(selected_tray)
                        self.print_emulation.tray.load(selected_tray, "Custom", MediaType.Plain.name,
                                                media_orientation="Portrait")
                        self.print_emulation.tray.close(selected_tray)
                        break

                if selected_tray is None:
                    raise ValueError("No tray found supporting anycustom size")
            else:
                default = self.tray.get_default_source()
                media_width_maximum = self.tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
                media_length_maximum = self.tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
                media_width_minimum = self.tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
                media_length_minimum = self.tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
                if self.tray.is_size_supported('anycustom', default):
                    self.tray.configure_tray(default, 'anycustom', 'stationery')
                elif self.tray.is_size_supported('custom', default) and media_width_maximum >= 527777 and media_length_maximum >= 351944 and  media_width_minimum <= 527777 and media_length_minimum <= 351944:
                    self.tray.configure_tray(default, 'custom', 'stationery') 

            job_id = self.print.raw.start('683a8528125ca09d8314435c051331de2b4c981c756721a2d12c103e8603a1d2', timeout=300)
            # Wait for copy job to complete
            self.print.wait_for_state(job_id, ["completed"])
            self.outputsaver.save_output()
            self.tray.reset_trays()
            logging.info("Jpeg file example JPG 1MB Page - Print job completed successfully")
