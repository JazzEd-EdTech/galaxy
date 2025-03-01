from .framework import (
    selenium_test,
    SeleniumTestCase,
)


class HistoryMultiViewTestCase(SeleniumTestCase):

    ensure_registered = True

    @selenium_test
    def test_display(self):
        history_id = self.current_history_id()
        input_collection = self.dataset_collection_populator.create_list_in_history(
            history_id, contents=["0", "1", "0", "1"], wait=True
        ).json()
        input_hid = input_collection["outputs"][0]["hid"]
        self.home()
        self.open_history_multi_view()
        hdca_selector = self.history_panel_wait_for_hid_state(input_hid, "ok", multi_history_panel=True)
        self.wait_for_visible(hdca_selector)
        self.screenshot("multi_history_collection")

    @selenium_test
    def test_list_list_display(self):
        history_id = self.current_history_id()
        method = self.dataset_collection_populator.create_list_of_list_in_history(history_id, wait=True).json
        self.prepare_multi_history_view(method)
        dataset_selector = self.history_panel_wait_for_hid_state(1, None, multi_history_panel=True)
        self.click(dataset_selector)
        dataset_selector = self.history_panel_wait_for_hid_state(3, None, multi_history_panel=True)
        self.click(dataset_selector)
        self.screenshot("multi_history_list_list")

    def prepare_multi_history_view(self, collection_populator_method):
        collection = collection_populator_method()
        if "outputs" in collection:
            collection = self.dataset_collection_populator.wait_for_fetched_collection(collection)
        collection_hid = collection["hid"]

        self.home()
        self.open_history_multi_view()
        selector = self.history_panel_wait_for_hid_state(collection_hid, "ok", multi_history_panel=True)
        self.click(selector)
        return selector
