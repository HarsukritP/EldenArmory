import React, { useState, useEffect } from 'react';

interface Weapon {
    name: string;
    type: string;
    physical_damage: number;
    magic_damage: number;
    fire_damage: number;
    light_damage: number;
    holy_damage: number;
    crit_damage: number;
    stamina_damage: number;
    strength_scaling: number;
    dexterity_scaling: number;
    intelligence_scaling: number;
    faith_scaling: number;
    arcane_scaling: number;
    weight: number;
    upgrade_type: string;
    value: number;
    image_url: string;
    description: string;
}

interface SortState {
    field: keyof Weapon | null;
    direction: 'asc' | 'desc' | null;
}

interface PlayerStats {
    strength: number;
    dexterity: number;
    intelligence: number;
    faith: number;
    arcane: number;
}

interface WeaponListProps {
  darkMode: boolean;
}

const INITIAL_STATS: PlayerStats = {
    strength: 10,
    dexterity: 10,
    intelligence: 10,
    faith: 10,
    arcane: 10
};

const WeaponList: React.FC<WeaponListProps> = ({ darkMode }) => {
    const [weapons, setWeapons] = useState<Weapon[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedType, setSelectedType] = useState('');
    const [sortState, setSortState] = useState<SortState>({
        field: 'physical_damage',
        direction: 'desc'
    });
    const [selectedWeapon, setSelectedWeapon] = useState<Weapon | null>(null);
    const [selectedForComparison, setSelectedForComparison] = useState<Weapon[]>([]);
    const [playerStats, setPlayerStats] = useState<PlayerStats>(INITIAL_STATS);
    const [weaponLevel, setWeaponLevel] = useState(1);

    const resetStats = () => {
        setWeaponLevel(0);
        setPlayerStats(INITIAL_STATS);
    };

    const handleWeaponSelect = (weapon: Weapon) => {
        resetStats();
        setSelectedWeapon(weapon);
    };

    const fetchWeapons = async () => {
        try {
            console.log('Fetching weapons...');
            const response = await fetch('http://localhost:5001/api/weapons');
            
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Server response: ${errorText}`);
            }
            
            const data = await response.json();
            console.log(`Loaded ${data.length} weapons`);
            setWeapons(data);
            if (data.length > 0) {
                handleWeaponSelect(data[0]);
            }
        } catch (err) {
            console.error('Error fetching weapons:', err);
            setError('Failed to load weapons');
        } finally {
            setLoading(false);
        }
    };

    const fetchUpdatedWeaponStats = async () => {
        if (!selectedWeapon) return;
        
        try {
            const encodedName = encodeURIComponent(selectedWeapon.name);
            const queryParams = new URLSearchParams({
                level: weaponLevel.toString(),
                strength: playerStats.strength.toString(),
                dexterity: playerStats.dexterity.toString(),
                intelligence: playerStats.intelligence.toString(),
                faith: playerStats.faith.toString(),
                arcane: playerStats.arcane.toString()
            });

            const url = `http://localhost:5001/api/weapons/${encodedName}?${queryParams}`;
            console.log('Fetching updated stats from:', url);

            const response = await fetch(url);
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error('Server response:', errorText);
                throw new Error(`Failed to fetch updated stats: ${response.status}`);
            }
            
            const updatedWeapon = await response.json();
            console.log('Updated weapon stats:', updatedWeapon);
            setSelectedWeapon(updatedWeapon);
        } catch (err) {
            console.error('Error updating weapon stats:', err);
        }
    };

    useEffect(() => {
        fetchWeapons();
    }, []);

    useEffect(() => {
        if (selectedWeapon) {
            fetchUpdatedWeaponStats();
        }
    }, [weaponLevel, playerStats]);

    const getBaseDamage = (weapon: Weapon) => {
      return weapon.physical_damage; // Just use the base physical damage for the list view
    };

    const handleComparisonToggle = (weapon: Weapon) => {
        setSelectedForComparison(prev => {
            const isSelected = prev.some(w => w.name === weapon.name);
            if (isSelected) {
                return prev.filter(w => w.name !== weapon.name);
            }
            if (prev.length >= 5) {
                alert('Maximum 5 weapons can be compared at once');
                return prev;
            }
            return [...prev, weapon];
        });
    };

    const handleSort = (field: keyof Weapon) => {
        setSortState(prev => {
            if (prev.field !== field) {
                return { field, direction: 'desc' };
            }
            if (prev.direction === 'desc') {
                return { field, direction: 'asc' };
            }
            return { field: null, direction: null };
        });
    };

    const getMaxLevel = (upgradeType: string) => {
        return upgradeType === 'Somber Smithing Stones' ? 10 : 25;
    };

    const handleStatChange = (stat: keyof PlayerStats, value: number) => {
        const clampedValue = Math.min(99, Math.max(1, value));
        setPlayerStats(prev => ({
            ...prev,
            [stat]: clampedValue
        }));
    };

    const getTotalDamage = (weapon: Weapon) => {
        return weapon.physical_damage + weapon.magic_damage + weapon.fire_damage + 
               weapon.light_damage + weapon.holy_damage;
    };

    const sortedWeapons = [...weapons]
        .filter(weapon => 
            weapon.name.toLowerCase().includes(searchTerm.toLowerCase()) &&
            (!selectedType || weapon.type === selectedType)
        )
        .sort((a, b) => {
            if (!sortState.field || !sortState.direction) return 0;
            
            const aVal = a[sortState.field];
            const bVal = b[sortState.field];
            
            if (aVal === undefined && bVal === undefined) return 0;
            if (aVal === undefined) return 1;
            if (bVal === undefined) return -1;
            
            const modifier = sortState.direction === 'asc' ? 1 : -1;
            
            if (typeof aVal === 'string' && typeof bVal === 'string') {
                return aVal.localeCompare(bVal) * modifier;
            }
            return ((aVal < bVal ? -1 : 1) * modifier);
        });

    const weaponTypes = Array.from(new Set(weapons.map(w => w.type))).sort();

    if (loading) return <div className="text-white text-lg">Loading weapons...</div>;
    if (error) return <div className="text-red-500 text-lg">{error}</div>;

    return (
        <div className="flex flex-col gap-6 p-4">
            <div className="flex flex-col lg:flex-row gap-6">  {/* Add flex-col and lg:flex-row */}
                {/* Left side - Weapon List */}
                <div className="w-full lg:w-1/2 h-[800px]">  {/* Update width classes */}
                    <div className="bg-gray-900 rounded-lg p-4 h-[980px]">  {/* Set fixed height */}
                        <div className="flex gap-4 mb-4">
                            <input
                                type="text"
                                placeholder="Search weapons..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                                className="flex-1 px-4 py-2 bg-gray-800 text-white rounded-lg
                                        border border-gray-700 focus:outline-none focus:border-blue-500
                                        placeholder-gray-400"
                            />
                            <select
                                value={selectedType}
                                onChange={(e) => setSelectedType(e.target.value)}
                                className="px-4 py-2 bg-gray-800 text-white rounded-lg
                                        border border-gray-700 focus:outline-none focus:border-blue-500"
                            >
                                <option value="">All Types</option>
                                {weaponTypes.map(type => (
                                    <option key={type} value={type}>{type}</option>
                                ))}
                            </select>
                        </div>

                        <div className="overflow-y-auto bg-gray-800 rounded-lg h-[885px]">
                            <table className="w-full">
                                <thead className="sticky top-0 bg-gray-700">
                                    <tr>
                                        <th className="w-8 px-2 py-3">
                                            {/* Checkbox column */}
                                        </th>
                                        {[
                                            { key: 'name', label: 'Name', align: 'left' },
                                            { key: 'type', label: 'Type', align: 'left' },
                                            { key: 'physical_damage', label: 'Physical', align: 'right' },
                                            { key: 'value', label: 'Rating', align: 'right' },
                                            { key: 'weight', label: 'Weight', align: 'right' }
                                        ].map(({ key, label, align }) => (
                                            <th
                                                key={key}
                                                onClick={() => handleSort(key as keyof Weapon)}
                                                className={`px-4 py-3 text-${align} text-sm font-semibold text-gray-200 
                                                        cursor-pointer hover:bg-gray-600 transition-colors`}
                                            >
                                                <div className={`flex items-center ${align === 'right' ? 'justify-end' : 'justify-start'}`}>
                                                    {label}
                                                    {sortState.field === key && sortState.direction && (
                                                        <span className="ml-2 text-blue-400">
                                                            {sortState.direction === 'asc' ? '↑' : '↓'}
                                                        </span>
                                                    )}
                                                </div>
                                            </th>
                                        ))}
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-gray-700">
                                    {sortedWeapons.map((weapon) => (
                                        <tr 
                                            key={weapon.name}
                                            onClick={() => handleWeaponSelect(weapon)}
                                            className={`hover:bg-gray-700 transition-colors cursor-pointer
                                                    ${selectedWeapon?.name === weapon.name ? 'bg-gray-700' : ''}`}
                                        >
                                            <td className="px-2 py-4">
                                                <input
                                                    type="checkbox"
                                                    className="w-4 h-4 rounded"
                                                    checked={selectedForComparison.some(w => w.name === weapon.name)}
                                                    onChange={() => handleComparisonToggle(weapon)}
                                                    onClick={(e) => e.stopPropagation()}
                                                />
                                            </td>
                                            <td className="px-4 py-4 text-white">{weapon.name}</td>
                                            <td className="px-4 py-4 text-gray-300">{weapon.type}</td>
                                            <td className="px-4 py-4 text-right text-white">{getBaseDamage(weapon)}</td>
                                            <td className="px-4 py-4 text-right text-blue-400">{weapon.value.toFixed(1)}%</td>
                                            <td className="px-4 py-4 text-right text-gray-300">{weapon.weight}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* Right side - Weapon Details */}
                {selectedWeapon && (
                    <div className="w-1/2">
                        <div className="bg-[#1a1f2e] rounded-lg p-6 flex-1">
                            <div className="text-center mb-6">
                                {selectedWeapon.image_url && (
                                    <div className="mb-4 h-64 flex items-center justify-center">
                                        <img 
                                            src={selectedWeapon.image_url}
                                            alt={selectedWeapon.name}
                                            className="max-h-full object-contain"
                                            onError={(e) => {
                                                const target = e.target as HTMLImageElement;
                                                target.style.display = 'none';
                                                console.error('Failed to load image:', selectedWeapon.image_url);
                                            }}
                                        />
                                    </div>
                                )}
                                <h2 className="text-3xl font-bold text-white">
                                    {selectedWeapon.name} {weaponLevel > 0 && `+${weaponLevel}`}
                                </h2>
                                {selectedWeapon.description && (
                                    <p className="text-gray-400 mt-2 italic">{selectedWeapon.description}</p>
                                )}
                                <p className="text-gray-400 mt-2">{selectedWeapon.type}</p>
                            </div>

                            <div className="grid grid-cols-2 gap-6">
                                {/* Attack Power Panel */}
                                <div className="bg-[#252a3d] rounded-lg p-5">
                                    <h3 className="text-xl font-bold text-white mb-4">Attack Power</h3>
                                    <div className="space-y-2">
                                        {[
                                            ['Physical', selectedWeapon.physical_damage],
                                            ['Magic', selectedWeapon.magic_damage],
                                            ['Fire', selectedWeapon.fire_damage],
                                            ['Light', selectedWeapon.light_damage],
                                            ['Holy', selectedWeapon.holy_damage],
                                            ['Critical', selectedWeapon.crit_damage],
                                            ['Stamina', selectedWeapon.stamina_damage],
                                        ].map(([label, value]) => (
                                            <div key={label} className="flex justify-between items-center">
                                                <span className="text-gray-400">{label}</span>
                                                <span className="text-white">{value}</span>
                                            </div>
                                        ))}
                                    </div>
                                    <h3 className="text-xl font-bold text-white py-4">Attribute Scaling</h3>
                                    <div className="space-y-2">
                                        {[
                                            ['Strength', selectedWeapon.strength_scaling],
                                            ['Dexterity', selectedWeapon.dexterity_scaling],
                                            ['Intelligence', selectedWeapon.intelligence_scaling],
                                            ['Faith', selectedWeapon.faith_scaling],
                                            ['Arcane', selectedWeapon.arcane_scaling],
                                        ].map(([label, value]) => (
                                            <div key={label} className="flex justify-between items-center">
                                                <span className="text-gray-400">{label}</span>
                                                <span className="text-white">{value}</span>
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                {/* Stats Panel */}
                                <div className="bg-[#252a3d] rounded-lg p-5">
                                <div className="mb-6">
    <h3 className="text-xl font-bold text-white mb-4">Weapon Level</h3>
    <div className="space-y-2">
        <div className="flex items-center gap-4">
            <input
                type="range"
                min="1"
                max={getMaxLevel(selectedWeapon.upgrade_type)}
                value={weaponLevel}
                onChange={(e) => setWeaponLevel(parseInt(e.target.value))}
                className="flex-1 h-2 bg-gray-700 rounded-lg appearance-none"
            />
            <input
                type="number"
                min="1"
                max={getMaxLevel(selectedWeapon.upgrade_type)}
                value={weaponLevel}
                onChange={(e) => {
                    const val = parseInt(e.target.value);
                    if (!isNaN(val)) {
                        setWeaponLevel(Math.min(Math.max(1, val), getMaxLevel(selectedWeapon.upgrade_type)));
                    }
                }}
                className="w-16 px-2 py-1 bg-gray-700 text-white rounded text-center"
            />
        </div>
        <div className="flex justify-between text-gray-400 text-sm">
            <span>1</span>
            <span>{getMaxLevel(selectedWeapon.upgrade_type)}</span>
        </div>
    </div>
</div>

                                    <div>
                                        <h3 className="text-xl font-bold text-white mb-4">Player Stats</h3>
                                        <div className="space-y-3">
                                        {Object.entries(playerStats).map(([stat, level]) => (
                                          <div key={stat} className="flex items-center justify-between">
                                              <span className="text-gray-400 capitalize">{stat}:</span>
                                              <div className="flex items-center gap-2">
                                                  <button
                                                      onClick={() => handleStatChange(stat as keyof PlayerStats, level - 1)}
                                                      className="w-8 h-8 bg-[#1a1f2e] text-white rounded-md hover:bg-[#2a2f3e]"
                                                  >
                                                      -
                                                  </button>
                                                  <input
                                                      type="number"
                                                      min="1"
                                                      max="99"
                                                      value={level}
                                                      onChange={(e) => {
                                                          const val = parseInt(e.target.value);
                                                          if (!isNaN(val)) {
                                                              handleStatChange(stat as keyof PlayerStats, Math.min(Math.max(1, val), 99));
                                                          }
                                                      }}
                                                      className="w-16 bg-gray-700 text-white rounded px-2 py-1 text-center"
                                                  />
                                                  <button
                                                      onClick={() => handleStatChange(stat as keyof PlayerStats, level + 1)}
                                                      className="w-8 h-8 bg-[#1a1f2e] text-white rounded-md hover:bg-[#2a2f3e]"
                                                  >
                                                      +
                                                  </button>
                                              </div>
                                          </div>
                                      ))}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* Comparison View */}
            {selectedForComparison.length > 0 && (
                <div className="bg-gray-900 rounded-lg p-4 mt-6">
                    <div className="flex justify-between items-center mb-4">
                        <h3 className="text-xl font-bold text-white">Weapon Comparison</h3>
                        <button 
                            onClick={() => setSelectedForComparison([])}
                            className="text-gray-400 hover:text-white"
                        >
                            Clear All
                        </button>
                    </div>
                    <div className="flex gap-4 overflow-x-auto pb-2">
                        {selectedForComparison.map(weapon => (
                            <div key={weapon.name} className="flex-1 min-w-[250px] bg-gray-800 p-4 rounded-lg">
                                <div className="text-center mb-4">
                                    <h4 className="font-bold text-white mb-2">{weapon.name}</h4>
                                    <p className="text-gray-400 text-sm">{weapon.type}</p>
                                </div>
                                <div className="space-y-4 text-sm">
                                    <div>
                                        <h5 className="font-semibold text-white mb-2">Attack Power</h5>
                                        <div className="space-y-1 text-gray-300">
                                            <p>Physical: <span className="text-white">{weapon.physical_damage}</span></p>
                                            <p>Magic: <span className="text-white">{weapon.magic_damage}</span></p>
                                            <p>Fire: <span className="text-white">{weapon.fire_damage}</span></p>
                                            <p>Holy: <span className="text-white">{weapon.holy_damage}</span></p>
                                            <p>Critical: <span className="text-white">{weapon.crit_damage}</span></p>
                                        </div>
                                    </div>
                                    <div>
                                        <h5 className="font-semibold text-white mb-2">Scaling</h5>
                                        <div className="space-y-1 text-gray-300">
                                            <p>Strength: <span className="text-white">{weapon.strength_scaling}</span></p>
                                            <p>Dexterity: <span className="text-white">{weapon.dexterity_scaling}</span></p>
                                            <p>Intelligence: <span className="text-white">{weapon.intelligence_scaling}</span></p>
                                            <p>Faith: <span className="text-white">{weapon.faith_scaling}</span></p>
                                            <p>Arcane: <span className="text-white">{weapon.arcane_scaling}</span></p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default WeaponList;