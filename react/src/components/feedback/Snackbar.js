import React, { useState, useEffect } from 'react';
import { Snackbar as MuiSnackbar } from '@mui/material';
import MuiAlert from '@mui/material/Alert';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';

const Alert = React.forwardRef(function Alert(props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

const Snackbar = ({
  open,
  message,
  onClose,
  severity,
  closeButton = false,
  autoHideDuration = 6000,
  anchorOrigin = { vertical: 'bottom', horizontal: 'center' }
}) => {
  const [snackbars, setSnackbars] = useState([]);

  useEffect(() => {
    if (open) {
      setSnackbars([{ message, severity }]);
    }
  }, [open, message, severity]);

  useEffect(() => {
    if (snackbars.length > 0) {
      const timer = setTimeout(() => {
        setSnackbars(prev => prev.slice(1));
        onClose();
      }, autoHideDuration);
      return () => clearTimeout(timer);
    }
  }, [snackbars, onClose, autoHideDuration]);

  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setSnackbars(prev => prev.slice(1));
    onClose();
  };

  return (
    <>
      {snackbars.map((snackbar, index) => (
        <MuiSnackbar
          key={index}
          anchorOrigin={anchorOrigin}
          open={index === 0}
          autoHideDuration={autoHideDuration}
          onClose={handleClose}
          action={
            closeButton ? (
              <IconButton
                size="small"
                aria-label="close"
                color="inherit"
                onClick={handleClose}
              >
                <CloseIcon fontSize="small" />
              </IconButton>
            ) : null
          }
        >
          <Alert
            onClose={handleClose}
            severity={snackbar.severity}
            sx={{ width: '100%' }}
          >
            {snackbar.message}
          </Alert>
        </MuiSnackbar>
      ))}
    </>
  );
};

export default Snackbar;