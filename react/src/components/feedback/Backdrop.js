import * as React from "react";
import MuiBackdrop from "@mui/material/Backdrop";
import CircularProgress from "@mui/material/CircularProgress";
import Button from "@mui/material/Button";
import PropTypes from "prop-types";

export default function Backdrop({
  buttonText = "Show backdrop",
  backdropColor = "#fff",
  zIndex = (theme) => theme.zIndex.drawer + 1,
  progressColor = "inherit",
  ...props
}) {
  const [open, setOpen] = React.useState(false);
  const handleClose = () => {
    setOpen(false);
  };
  const handleOpen = () => {
    setOpen(true);
  };

  return (
    <div>
      <Button onClick={handleOpen}>{buttonText}</Button>
      <MuiBackdrop
        sx={(theme) => ({ color: backdropColor, zIndex: zIndex(theme) })}
        open={open}
        onClick={handleClose}
        {...props}
      >
        <CircularProgress color={progressColor} />
      </MuiBackdrop>
    </div>
  );
}

Backdrop.propTypes = {
  buttonText: PropTypes.string,
  backdropColor: PropTypes.string,
  zIndex: PropTypes.oneOfType([PropTypes.number, PropTypes.func]),
  progressColor: PropTypes.string,
};