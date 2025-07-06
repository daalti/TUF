from dunetuf.job.job_history.job_history import JobHistory
from dunetuf.job.job_queue.job_queue import JobQueue
from dunetuf.print.print_new import Print
import logging

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
        +purpose:Simple print job of Jpeg testprog Page from *testprog.jpg file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:testprog.jpg=24770f706b81b40a71944af3b39aad8a3f7ffb21c4f2725447022e518222d823
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_testprog_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_testprog
            +guid:8775816e-5b43-4867-a7db-7dc5aa1ee11b
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG
    

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$

    """
    def test_when_using_testprog_then_succeeds(self):
            expected_state = 'SUCCESS'

            response = self.cdm.get(self.cdm.CDM_MEDIA_CAPABILITIES)

            media_source= response['supportedInputs'][0]['mediaSourceId']
            resolution = response['supportedInputs'][0]['resolution']
            bottom_margin= response['supportedInputs'][0]['minimumPhysicalBottomMargin']/resolution
            top_margin= response['supportedInputs'][0]['minimumPhysicalTopMargin']/resolution
            left_margin= response['supportedInputs'][0]['minimumPhysicalLeftMargin']/resolution
            right_margin= response['supportedInputs'][0]['minimumPhysicalRightMargin']/resolution
            image_width=227/600  #Didn't have an option to get raw resolution of the image so using 600 as defualt resolution
            image_height=149/600

            if("roll" in media_source):
                if(image_width<(left_margin+right_margin) or image_height<(top_margin+bottom_margin)):
                    expected_state='FAILED'

            self.outputsaver.validate_crc_tiff(self.udw)
            job_id = self.print.raw.start('24770f706b81b40a71944af3b39aad8a3f7ffb21c4f2725447022e518222d823',expected_job_state=expected_state, timeout=120)
            # Wait for copy job to complete
            self.print.wait_for_state(job_id, ["completed"])
            self.outputsaver.save_output()
            Current_crc_value = self.outputsaver.get_crc()
            logging.info("Validate current crc with master crc")
            assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

            logging.info("JPEG testprog Page- Print job completed successfully")
