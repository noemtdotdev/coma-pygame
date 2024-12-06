import * as React from "react";
import MuiAlert from "@mui/material/Alert";
import CheckIcon from "@mui/icons-material/Check";
import CloseIcon from "@mui/icons-material/Close";
import IconButton from "@mui/material/IconButton";
import PropTypes from "prop-types";

export default function Alert({
  severity = "success",
  message = "Here is a gentle confirmation that your action was successful.",
  icon = <CheckIcon fontSize="inherit" />,
  onClose,
  variant = "filled",
  closeButton = false,
  ...props
}) {
  return (
    <MuiAlert
      icon={icon}
      severity={severity}
      onClose={onClose}
      variant={variant}
      action={
        closeButton ? (
          <IconButton
            size="small"
            aria-label="close"
            color="inherit"
            onClick={onClose}
          >
            <CloseIcon fontSize="small" />
          </IconButton>
        ) : null
      }
      {...props}
    >
      {message}
    </MuiAlert>
  );
}

Alert.propTypes = {
  severity: PropTypes.oneOf(["error", "warning", "info", "success"]),
  message: PropTypes.string,
  icon: PropTypes.element,
  onClose: PropTypes.func,
  variant: PropTypes.oneOf(["filled", "outlined", "standard"]),
  closeButton: PropTypes.bool,
};