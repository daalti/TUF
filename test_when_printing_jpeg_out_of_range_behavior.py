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
        +purpose:Test jpeg out of range behavior on roll
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-155289
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:A0-600-L.jpg=b9d02741fadecd94d682bb8b40ec433f5ab27ef63418cdcea21085d7b4e89d90
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_out_of_range_behavior_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_out_of_range_behavior_on_roll
            +guid:0ef9c857-0d81-488b-9a31-13e401744536
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & MediaInputInstalled=MainRoll & MediaInputInstalled=Main
    

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$

    """
    def test_when_using_out_of_range_behavior_then_succeeds(self):
            self.tray.unload_media()

            #Input document is landscape A0 size. It will be printed on roll by rotating it to portrait.
            ipp_test_attribs = {
                'document-format': 'image/jpeg',
                'media-size-name': 'iso_a0_841x1189mm',
                'media-source': 'main-roll'
            }

            ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)
            jobid = printjob.start_ipp_print(ipp_test_file, 'b9d02741fadecd94d682bb8b40ec433f5ab27ef63418cdcea21085d7b4e89d90')

            if self.tray.is_size_supported('iso_a0_841x1189mm', 'main-roll'):
                self.media.wait_for_alerts('mediaLoadFlow', 100)
                self.tray.configure_tray('main-roll', 'iso_a0_841x1189mm', 'stationery')
                self.tray.load_media('main-roll')
                self.media.alert_action('mediaLoadFlow', 'ok')

            printjob.wait_verify_job_completion(jobid, "SUCCESS", timeout=300)

            self.outputverifier.save_and_parse_output()
            self.tray.reset_trays()
            self.tray.unload_media()  # Will unload self.media from all trays
            self.tray.load_media()  # Will load self.media in all trays to default

            self.outputverifier.verify_media_source(Intents.printintent, MediaSource.mainroll)
            self.outputverifier.verify_media_size(Intents.printintent, MediaSize.a0)

            # CRC check
            self.outputsaver.operation_mode('TIFF')
            self.outputsaver.validate_crc_tiff(self.udw)
            logging.info("Get crc value for the current print job")
            Current_crc_value = self.outputsaver.get_crc()
            logging.info("Validate current crc with master crc")
            assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
            self.outputsaver.operation_mode('NONE')
