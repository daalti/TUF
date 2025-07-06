from dunetuf.job.job_history.job_history import JobHistory
from dunetuf.job.job_queue.job_queue import JobQueue
from dunetuf.print.print_new import Print
import logging
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding

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
        +purpose:Test jpeg small job on large paper tray
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-153638
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:abbey-4x6-L.jpg=1fcc44e51d4702a75c0487be852ae62fca82a2cab4bf0d19645b83e3264eb1d0
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_smalljob_on_largepaper_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_smalljob_on_largepaper_on_tray
            +guid:2590acaa-905d-4eb9-b431-47a7bf4f4e5e
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & MediaInputInstalled=MainRoll & MediaInputInstalled=Main
    

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$

    """
    def test_when_using_smalljob_on_largepaper_then_succeeds(self):
            self.tray.unload_media()
            if self.tray.is_size_supported('iso_a4_210x297mm', 'main'):
                self.tray.configure_tray('main', 'iso_a4_210x297mm', 'stationery')
                self.tray.load_media('main')

            ipp_test_attribs = {
                'document-format': 'image/jpeg',
                'media-source': 'main'
            }

            ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)
            jobid = printjob.start_ipp_print(ipp_test_file, '1fcc44e51d4702a75c0487be852ae62fca82a2cab4bf0d19645b83e3264eb1d0')

            printjob.wait_verify_job_completion(jobid, "SUCCESS", timeout=180)

            self.outputverifier.save_and_parse_output()
            self.tray.reset_trays()
            self.tray.unload_media()  # Will unload self.media from all trays
            self.tray.load_media()  # Will load self.media in all trays to default

            self.outputverifier.verify_media_source(Intents.printintent, MediaSource.main)
            self.outputverifier.verify_media_size(Intents.printintent, MediaSize.a4)  # coming as a4 due to jpeg scaling

            # CRC check
            self.outputsaver.operation_mode('TIFF')
            self.outputsaver.validate_crc_tiff(self.udw)
            logging.info("Get crc value for the current print job")
            Current_crc_value = self.outputsaver.get_crc()
            logging.info("Validate current crc with master crc")
            assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
            self.outputsaver.operation_mode('NONE')
