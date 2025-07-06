from dunetuf.job.job_history.job_history import JobHistory
from dunetuf.job.job_queue.job_queue import JobQueue
from dunetuf.print.print_new import Print
import logging
@pytest.fixture(autouse=True)
def setup_teardown_pdl_test(job, usbdevice):
    #override setup to prevent reset of roll length
    if not self.usbdevice.devices('frontUsb'):
        logging.info('Adding USB mock device')
        self.usbdevice.add_mock_device('usbdisk1', 'UsbDisk1', 'frontUsb')
    logging.info("Cancel all active jobs")
    self.job.cancel_active_jobs()
    logging.info("Wait for no active jobs")
    self.job.wait_for_no_active_jobs()
    yield
    if self.usbdevice.check_device('usbdisk1'):
        self.usbdevice.remove_mock_device('usbdisk1')
    logging.info("Cancel all active jobs")
    self.job.cancel_active_jobs()
    logging.info("Wait for no active jobs")
    self.job.wait_for_no_active_jobs()

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
        +purpose: Test Print From Thumb drive for jpeg file with Custom size configured
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid: DUNE-218422
        +timeout: 600
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework: TUF
        +external_files:5x7in_1_1006.jpg=0fdbac1601827141ec0cb70960c57ea887089bd65b60dde7f0d4ddeb7841bc84
        +name:TestWhenPrintingJPEGFile::test_when_using_printfromusb_custom_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title: test_jpeg_printfromusb_custom
            +guid:299df654-1118-4aa4-ab6f-a1415c101b92
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=JPEG & DeviceFunction=PrintFromUsb & ConsumableSupport=Ink & MediaInputInstalled=Tray1
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$

    """
    def test_when_using_printfromusb_custom_then_succeeds(self):
            # Upload required images to simulated usb device
            self.outputsaver.operation_mode('CRC')
            usbroot = self.usbdevice.get_root('usbdisk1')
            filepath = self.usbdevice.upload('0fdbac1601827141ec0cb70960c57ea887089bd65b60dde7f0d4ddeb7841bc84', usbroot)

            logging.info('Creating print from USB job ticket')
            resource = {'src': {'usb': {}}, 'dest': {'print': {}}}
            ticketId = self.job.create_job_ticket(resource)

            default = self.tray.get_default_source()
            mediasize = 'custom'
            if self.tray.is_size_supported('na_5x7_5x7in', default):
                self.tray.configure_tray(default, 'na_5x7_5x7in', 'stationery')

            resource = {
                'src': {
                    'usb': {'path': filepath}
                },
                'dest': {
                    'print': {
                        'mediaSource': default,
                        'mediaSize': mediasize,
                        'mediaType': 'stationery',
                    }
                },
                }

            logging.info('Updating print from USB job ticket with source and destination')
            self.job.update_job_ticket(ticketId, resource)

            logging.info('Create a print job and retrieve print job id')
            jobId = self.job.create_job(ticketId)

            logging.info('Initialize and start the print job - %s', jobId)
            self.job.change_job_state(jobId, 'initialize', 'initializeProcessing')
            self.job.check_job_state(jobId, 'ready', 30)
            self.job.change_job_state(jobId, 'start', 'startProcessing')

            jobstate = self.job.wait_for_job_completion_cdm(jobId, 120)
            expected_crc = ["0x5d91f7bc"]
            self.outputsaver.verify_output_crc(expected_crc)

            self.outputsaver.save_output()
            self.outputsaver.operation_mode('NONE')
            assert 'success' in jobstate, 'Unexpected final job state!'
