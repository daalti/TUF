from dunetuf.job.job_history.job_history import JobHistory
from dunetuf.job.job_queue.job_queue import JobQueue
from dunetuf.print.print_new import Print
import logging
from dunetuf.print.print_common_types import MediaSize, MediaType

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
        +purpose:C52178011 Simple print job of Jpeg Regression of untagged argb 100dpi Page from *untagged_argb_100dpi.jpg file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:400
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:untagged_argb_100dpi.jpg=d91801b4c08f2ed918a3cbf885a61c8721cace99b0e83a2f82e95660e2275704
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_regression_untagged_argb_100dpi_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_regression_untagged_argb_100dpi
            +guid:27528ced-c583-4fea-bad4-4f1bc5120fc5
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
            +ProA4:
                +is_manual:False
                +timeout:600
                +test:
                    +dut:
                        +type:Emulator
        +overrides:
            +Home:
                +is_manual:False
                +timeout:600
                +test:
                    +dut:
                        +type:Engine
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$

    """
    def test_when_using_regression_untagged_argb_100dpi_then_succeeds(self):
            if self.outputsaver.configuration.productname == "jupiter":
                self.outputsaver.operation_mode('CRC')
            else:
                self.outputsaver.operation_mode('TIFF')

            if self.print_emulation.print_engine_platform == 'emulator':
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
                if self.tray.is_size_supported('any', default):
                    tray_test_name = self.print_mapper.get_media_input_test_name(default)
                    self.print_emulation.tray.setup_tray(tray_test_name, MediaSize.Letter.name, MediaType.Plain.name)
                    self.tray.configure_tray(default, 'any', 'any')
                elif self.tray.is_size_supported('anycustom', default):
                    self.tray.configure_tray(default, "anycustom", 'stationery')
                else:
                    media_width_maximum = self.tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
                    media_length_maximum = self.tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
                    media_width_minimum = self.tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
                    media_length_minimum = self.tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
                    if self.tray.is_size_supported('custom', default) and media_width_maximum >= 527777 and media_length_maximum >= 351944 and media_width_minimum <= 527777 and media_length_minimum <= 351944:
                        self.tray.configure_tray(default, 'custom', 'stationery')
                    else:
                        self.tray.configure_tray(default, 'custom', 'stationery')

            self.outputsaver.validate_crc_tiff(self.udw) 
            job_id = self.print.raw.start('d91801b4c08f2ed918a3cbf885a61c8721cace99b0e83a2f82e95660e2275704',timeout=360)
            # Wait for copy job to complete
            self.print.wait_for_state(job_id, ["completed"])

            self.outputsaver.save_output()
            if self.outputsaver.configuration.productname == "jupiter":
                expected_crc = ["0x9350fdc4"]    
                self.outputsaver.verify_output_crc(expected_crc)
            logging.info("Get crc value for the current print job")
            Current_crc_value = self.outputsaver.get_crc() 
            logging.info("Validate current crc with master crc")
            assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
            self.outputsaver.operation_mode('NONE')
            self.tray.reset_trays()

            logging.info("JPEG Regression untagged argb 100dpi Page - Print job completed successfully")
