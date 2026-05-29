from ORION import run_orion, open_search
import threading

def controller_run_orion(self):
        
        if not self.lock.acquire(blocking = False):
            print("ORION is already running")
            return
        
        
        threading.Lock() = True 

        self.set_state(self.SEARCHING)
        def task():

            try:

                result = run_orion()


                print(result)

                if result:
                    self.set_state(self.RESPONDING)
                    open_search(result["intent"])

            except Exception as e:

                print("Error:", e)

            finally:
                self.set_state(self.IDLE)
                self.lock.realase()

        thread = threading.Thread(
            target=task,
            daemon=True
    )

        thread.start()