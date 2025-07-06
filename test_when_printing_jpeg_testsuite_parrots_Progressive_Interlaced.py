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
        +purpose:C52178010 Simple print job of Jpeg TestSuite parrots Progressive Interlaced Page from *parrots_Progressive_Interlaced.jpg file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:660
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:parrots_Progressive_Interlaced.jpg=dfcaa88adf10d6833f97280b5a58893db02845db6c41495cd324ccb1145bda9a
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_testsuite_parrots_Progressive_Interlaced_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_testsuite_parrots_Progressive_Interlaced
            +guid:b98580dc-6267-4698-8f74-ab6e05916f49
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG
        +overrides:
            +Home:
                +is_manual:False
                +timeout:660
                +test:
                    +dut:
                        +type:Engine
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$

    """
    def test_when_using_testsuite_parrots_Progressive_Interlaced_then_succeeds(self):
            # Print file size : width 10.67 inches and height 7.11 inches
            default = self.tray.get_default_source()
            if self.tray.is_size_supported('anycustom', default):
                self.tray.configure_tray(default, 'anycustom', 'stationery')
            elif self.tray.is_size_supported('any', default):
                tray_test_name = self.print_mapper.get_media_input_test_name(default)
                self.print_emulation.tray.setup_tray(tray_test_name, MediaSize.Letter.name, MediaType.Plain.name)
                self.tray.configure_tray(default, 'any', 'any')
            else:
                self.tray.configure_tray(default, 'custom', 'stationery')
            self.outputsaver.validate_crc_tiff(self.udw) 
            job_id = self.print.raw.start('dfcaa88adf10d6833f97280b5a58893db02845db6c41495cd324ccb1145bda9a', timeout=600)
            # Wait for copy job to complete
            self.print.wait_for_state(job_id, ["completed"])
            self.outputsaver.save_output()
            logging.info("Get crc value for the current print job")
            Current_crc_value = self.outputsaver.get_crc() 
            logging.info("Validate current crc with master crc")
            assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
            self.tray.reset_trays()
            logging.info("JPEG TestSuite parrots Progressive Interlaced Page - Print job completed successfully")
