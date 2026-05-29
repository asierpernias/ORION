import threading

from ORION import run_orion, open_search


def controller_run_orion(self):

    if not self.lock.acquire(blocking=False):
        print("ORION is already running")
        return

    def task():

        try:
            self.request_state(self.SEARCHING)

            result = run_orion(ui=self)

            print(result)

            if result:
                self.request_state(self.RESPONDING)
                open_search(result["intent"])

        except Exception as e:
            print("Error:", e)

        finally:
            self.request_state(self.IDLE)
            self.lock.release()

    thread = threading.Thread(
        target=task,
        daemon=True
    )

    thread.start()