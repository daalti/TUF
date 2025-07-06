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
        +purpose:Simple print job of Jpeg TestSuite taggedRGB Page from *taggedRGB.jpg file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:taggedRGB.jpg=34027bf1e1808b1cf5995aedea2a805a35b12f77eb725ebb44dc662715fc295c
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_testsuite_taggedRGB_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_testsuite_taggedRGB
            +guid:eca4285c-f468-440a-958b-e2fbb388255a
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
    def test_when_using_testsuite_taggedRGB_then_succeeds(self):
            expected_state = 'SUCCESS'

            response = self.cdm.get(self.cdm.CDM_MEDIA_CAPABILITIES)

            media_source= response['supportedInputs'][0]['mediaSourceId']
            resolution = response['supportedInputs'][0]['resolution']
            bottom_margin= response['supportedInputs'][0]['minimumPhysicalBottomMargin']/resolution
            top_margin= response['supportedInputs'][0]['minimumPhysicalTopMargin']/resolution
            left_margin= response['supportedInputs'][0]['minimumPhysicalLeftMargin']/resolution
            right_margin= response['supportedInputs'][0]['minimumPhysicalRightMargin']/resolution
            image_width=499/600  #Didn't have an option to get raw resolution of the image so using 600 as defualt resolution
            image_height=202/600

            if("roll" in media_source):
                if(image_width<(left_margin+right_margin) or image_height<(top_margin+bottom_margin)):
                    expected_state='FAILED'
            job_id = self.print.raw.start('34027bf1e1808b1cf5995aedea2a805a35b12f77eb725ebb44dc662715fc295c', expected_job_state=expected_state)
            # Wait for copy job to complete
            self.print.wait_for_state(job_id, ["completed"])
            self.outputsaver.save_output()

            logging.info("JPEG TestSuite taggedRGB Page - Print job completed successfully")
