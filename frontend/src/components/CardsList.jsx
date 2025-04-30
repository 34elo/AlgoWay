import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon
} from '@mui/material';
import {
  Flight as FlightIcon,
  Train as TrainIcon,
  DirectionsBus as BusIcon,
  DirectionsCar as CarIcon,
  Schedule as TimeIcon,
  AttachMoney as MoneyIcon,
  Star as StarIcon,
  Place as PlaceIcon,
  ArrowRightAlt as ArrowIcon
} from '@mui/icons-material';


const transportIcons = {
  plane: <FlightIcon fontSize="small" />,
  train: <TrainIcon fontSize="small" />,
  bus: <BusIcon fontSize="small" />,
  car: <CarIcon fontSize="small" />,
};

const cardStyles = {
  mb: 3,
  borderRadius: 2,
  boxShadow: 3,
  transition: 'all 0.3s ease',
  '&:hover': {
    boxShadow: 6,
    transform: 'translateY(-2px)'
  }
};

const CardsList = ({ routes }) => {
  const formatTime = (minutes) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours > 0 ? `${hours} ч ` : ''}${mins} мин`;
  };

  return (
    <>
      <Typography variant="h5" gutterBottom sx={{
        fontWeight: 'bold',
        display: 'flex',
        alignItems: 'center',
        gap: 1,
        mb: 3
      }}>
        {routes.length} Найдено
      </Typography>

      {routes.map((route, index) => (
        <Card key={index} sx={cardStyles}>
          <CardContent>
            <Box sx={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              mb: 2
            }}>
              <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                Маршрут #{index + 1}
              </Typography>
              <Box sx={{ display: 'flex', gap: 1 }}>
                {route.transport.map((t, i) => (
                  <React.Fragment key={i}>
                    {transportIcons[t] || t}
                    {i < route.transport.length - 1 && <ArrowIcon />}
                  </React.Fragment>
                ))}
              </Box>
            </Box>

            <Box sx={{
              display: 'flex',
              gap: 2,
              flexWrap: 'wrap',
              mb: 2
            }}>
              <Chip
                icon={<TimeIcon />}
                label={formatTime(route.total_time)}
                color="info"
                variant="outlined"
              />
              <Chip
                icon={<MoneyIcon />}
                label={`${route.total_cost} руб`}
                color="success"
                variant="outlined"
              />
              <Chip
                icon={<StarIcon />}
                label={`${route.avg_comfort.toFixed(1)}/100`}
                color="warning"
                variant="outlined"
              />
            </Box>
            <Box sx={{
              display: 'flex',
              alignItems: 'center',
              p: 1.5,
              bgcolor: 'action.hover',
              borderRadius: 1,
              mb: 2
            }}>
              <PlaceIcon color="primary" sx={{ mr: 1 }} />
              <Typography>
                {route.path.join(' → ')}
              </Typography>
            </Box>
            {route.segments && (
              <Box>
                <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 'bold' }}>
                  Этапы маршрута:
                </Typography>
                <List disablePadding>
                  {route.segments.map((segment, segIndex) => (
                    <React.Fragment key={segIndex}>
                      <ListItem alignItems="flex-start" sx={{ px: 0 }}>
                        <ListItemIcon sx={{ minWidth: 32, color: 'text.secondary' }}>
                          {transportIcons[segment.transport] || segment.transport}
                        </ListItemIcon>
                        <ListItemText
                          primary={`${segment.from_city} → ${segment.to_city}`}
                          secondary={
                            <Box sx={{
                              display: 'flex',
                              gap: 1,
                              mt: 0.5,
                              flexWrap: 'wrap'
                            }}>
                              <Typography variant="caption" component="span">
                                {formatTime(segment.time)}
                              </Typography>
                              <Typography variant="caption" component="span">
                                • {segment.cost} руб •
                              </Typography>
                              <Typography variant="caption" component="span">
                                Комфорт: {segment.comfort}/100
                              </Typography>
                            </Box>
                          }
                        />
                      </ListItem>
                      {segIndex < route.segments.length - 1 && (
                        <Divider variant="inset" component="li" />
                      )}
                    </React.Fragment>
                  ))}
                </List>
              </Box>
            )}
          </CardContent>
        </Card>
      ))}
    </>
  );
};

export default CardsList;