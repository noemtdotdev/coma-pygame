import * as React from 'react';
import MuiCircularProgress from '@mui/material/CircularProgress';
import MuiLinearProgress from '@mui/material/LinearProgress';
import Box from '@mui/material/Box';
import PropTypes from 'prop-types';

export function CircularProgress({
  size = 40,
  thickness = 3.6,
  color = 'primary',
  value = 0,
  variant = 'indeterminate',
  ...props
}) {
  return (
    <Box sx={{ display: 'flex' }}>
      <MuiCircularProgress
        size={size}
        thickness={thickness}
        color={color}
        value={value}
        variant={variant}
        {...props}
      />
    </Box>
  );
}

CircularProgress.propTypes = {
  size: PropTypes.number,
  thickness: PropTypes.number,
  color: PropTypes.oneOf(['primary', 'secondary', 'inherit']),
  value: PropTypes.number,
  variant: PropTypes.oneOf(['determinate', 'indeterminate', 'static']),
};

export function LinearProgress({
  color = 'primary',
  value = 0,
  variant = 'indeterminate',
  ...props
}) {
  return (
    <Box sx={{ width: '100%' }}>
      <MuiLinearProgress
        color={color}
        value={value}
        variant={variant}
        {...props}
      />
    </Box>
  );
}

LinearProgress.propTypes = {
  color: PropTypes.oneOf(['primary', 'secondary', 'inherit']),
  value: PropTypes.number,
  variant: PropTypes.oneOf(['determinate', 'indeterminate', 'buffer', 'query']),
};