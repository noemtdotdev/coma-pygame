import React, { useState } from "react";
import Header from "../components/Header";
import Footer from "../components/Footer";
import Snackbar from "../components/feedback/Snackbar";
import Alert from "../components/feedback/Alert";
import Backdrop from "../components/feedback/Backdrop";
import {
  CircularProgress,
  LinearProgress,
} from "../components/feedback/Progess";

const Test = () => {
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");
  const [snackbarSeverity, setSnackbarSeverity] = useState("success");

  const handleSnackbarOpen = (message, severity) => {
    setSnackbarMessage(message);
    setSnackbarSeverity(severity);
    setSnackbarOpen(true);
  };

  const handleSnackbarClose = () => {
    setSnackbarOpen(false);
  };

  return (
    <div className="flex flex-col min-h-screen text-white">
      <Header />
      <main className="flex-grow">
        <button
          onClick={() =>
            handleSnackbarOpen("This is a success message!", "success")
          }
          className="bg-blue-500 text-white p-2 rounded"
        >
          Show Success Snackbar
        </button>
        <button
          onClick={() =>
            handleSnackbarOpen("This is an error message!", "error")
          }
          className="bg-red-500 text-white p-2 rounded ml-4"
        >
          Show Error Snackbar
        </button>
        <Snackbar
          open={snackbarOpen}
          message={snackbarMessage}
          onClose={handleSnackbarClose}
          severity={snackbarSeverity}
          closeButton={true}
          autoHideDuration={6000}
          anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
        />

        <Alert
          severity="error"
          message="This is an error message."
          closeButton={true}
          id="error-alert"
          onClose={() =>
            (document.getElementById("error-alert").style.display = "none")
          }
        />
        <Alert
          severity="info"
          message="This is an info message."
          closeButton={false}
        />

        <div>
          <Backdrop
            buttonText="Open Backdrop"
            backdropColor="rgba(0, 0, 0, 0.5)"
            zIndex={(theme) => theme.zIndex.modal + 1}
            progressColor="primary"
          />
        </div>
        <div>
          <CircularProgress
            size={50}
            thickness={5}
            color="secondary"
            value={75}
            variant="indeterminate"
          />
          <LinearProgress color="secondary" value={50} variant="determinate" />
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default Test;
