import {
    Autocomplete,
    TextField,
    Button,
    Box,
    Typography,
    Container,
    Radio,
    FormControl,
    FormLabel,
    RadioGroup,
    FormControlLabel,
    InputAdornment,
    Grid
} from "@mui/material";
import {useState, useEffect} from "react";
import axios from "axios";
import CardsList from "./CardsList.jsx";

export default function SelectionMenu() {
    const [cities, setCities] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [routes, setRoutes] = useState([]);
    const [selectedCities, setSelectedCities] = useState({
        from: null,
        to: null
    });
    const [typeRoute, setTypeRoute] = useState('');
    const [filters, setFilters] = useState({
        maxPrice: '',
        minComfort: ''
    });

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/cities/')
            .then(response => {
                setCities(response.data);
                setLoading(false);
            })
            .catch(error => {
                setError(error.message);
                setLoading(false);
            });
    }, []);

    const handleCityChange = (type) => (event, value) => {
        setSelectedCities(prev => ({
            ...prev,
            [type]: value
        }));
    };

    const handleFilterChange = (field) => (event) => {
        const value = event.target.value;
        // Проверяем, что вводится число или пустая строка
        if (value === '' || /^\d+$/.test(value)) {
            setFilters(prev => ({
                ...prev,
                [field]: value
            }));
        }
    };

    const searchRoutes = () => {
        if (!selectedCities.from || !selectedCities.to) {
            setError("Выберите города отправления и назначения");
            return;
        }
        if (selectedCities.from === selectedCities.to) {
            setError('Выберите другой город')
            return;
        }
        if (typeRoute === '') {
            setError('Выберите метод сортировки');
            return;
        }

        setLoading(true);
        const params = {
            from_city: selectedCities.from,
            to_city: selectedCities.to
        };

        if (filters.maxPrice) params.max_price = filters.maxPrice;
        if (filters.minComfort) params.min_comfort = filters.minComfort;

        axios.get(`http://127.0.0.1:8000/api/routes/${typeRoute}/`, {
            params: params,
            headers: {
                'Accept': 'application/json'
            }
        })
            .then(response => {
                if (response.data.length === 0) {
                    setError('Доступных путей нет');
                    return
                }
                setRoutes(response.data);
                setError(null);
            })
            .catch(error => {
                setError(error.message);
                setRoutes([]);
            })
            .finally(() => {
                setLoading(false);
            });
    };

    const handleChange = (event) => {
        setTypeRoute(event.target.value)
    }

    return (
        <Container
            sx={{
                display: 'flex',
                flexDirection: 'row',
                justifyContent: 'center',
                py: 4,
                overflow: 'scroll'
            }}
        >
            <Box
                sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    gap: 3,
                    p: 4,
                    boxShadow: 3,
                    borderRadius: 2,
                    bgcolor: 'background.paper',
                    maxHeight: '100%',
                }}
            >
                <Typography variant="h4" component="h1" gutterBottom align="center">
                    Путеводитель
                </Typography>

                {error && (
                    <Typography
                        color="error"
                        align="center"
                        sx={{width: '100%', mb: 2}}
                    >
                        {error}
                    </Typography>
                )}

                <Box sx={{width: '100%', display: 'flex', flexDirection: 'column', gap: 2}}>
                    <Autocomplete
                        id="from"
                        options={cities}
                        value={selectedCities.from}
                        onChange={handleCityChange('from')}
                        renderInput={(params) => (
                            <TextField {...params} label="Откуда" fullWidth/>
                        )}
                        disabled={loading}
                    />

                    <Autocomplete
                        id="to"
                        options={cities}
                        value={selectedCities.to}
                        onChange={handleCityChange('to')}
                        renderInput={(params) => (
                            <TextField {...params} label="Куда" fullWidth/>
                        )}
                        disabled={loading}
                    />
                </Box>

                <Box sx={{width: '100%'}}>
                    <FormControl fullWidth>
                        <FormLabel>Сортировать по</FormLabel>
                        <RadioGroup row onChange={handleChange}>
                            <FormControlLabel value="fastest" control={<Radio/>} label="Скорости"/>
                            <FormControlLabel value="comfort" control={<Radio/>} label="Комфорту"/>
                            <FormControlLabel value="cheapest" control={<Radio/>} label="Стоимости"/>
                        </RadioGroup>
                    </FormControl>
                </Box>

                <Box style={{
                    display: 'flex',
                    flexDirection: 'column',
                    width: '100%'
                }}>
                    <TextField
                        label="Макс. стоимость"
                        value={filters.maxPrice}
                        onChange={handleFilterChange('maxPrice')}
                        fullWidth
                        InputProps={{
                            endAdornment: <InputAdornment position="end"></InputAdornment>,
                        }}
                    />
                    <TextField
                        style={{
                            marginTop: '20px'
                        }}
                        label="Мин. комфорт"
                        value={filters.minComfort}
                        onChange={handleFilterChange('minComfort')}
                        fullWidth
                        InputProps={{
                            endAdornment: <InputAdornment position="end">/100</InputAdornment>,
                        }}
                    />
                </Box>

                <Button
                    variant="contained"
                    size="large"
                    onClick={searchRoutes}
                    disabled={loading || !selectedCities.from || !selectedCities.to}
                    sx={{width: '100%', py: 1.5}}
                >
                    {loading ? 'Поиск...' : 'Найти маршруты'}
                </Button>
                <Button small onClick={() => setRoutes([])}>Сброс</Button>
            </Box>

            {routes.length > 0 && (
                <Box
                    sx={{
                        minWidth: '500px',
                        display: 'flex',
                        width: '100%',
                        marginLeft: '20px',
                        padding: '25px',
                        flexDirection: 'column',
                        alignItems: 'center',
                        boxShadow: 3,
                        borderRadius: 2,
                        bgcolor: 'background.paper',
                        overflowX: 'scroll'
                    }}
                >
                    <CardsList routes={routes}/>
                </Box>
            )}
        </Container>
    );
}